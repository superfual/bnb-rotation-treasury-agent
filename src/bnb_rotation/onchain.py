"""Testnet-only owner-reviewed treasury rebalancing. Never signs or sends."""
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

CHAIN = 97
SELECTORS = {"balance": "70a08231", "allowance": "dd62ed3e", "decimals": "313ce567",
             "quote": "d06ca61f", "approve": "095ea7b3", "swap": "38ed1739"}


def address(value):
    if not isinstance(value, str) or not re.fullmatch(r"0x[0-9a-fA-F]{40}", value) or int(value, 16) == 0:
        raise ValueError("invalid nonzero address")
    return value.lower()


def number(value):
    if isinstance(value, (bool, float)):
        raise ValueError("use exact decimal strings")
    try:
        result = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("invalid decimal") from None
    if not result.is_finite() or result < 0:
        raise ValueError("nonfinite or negative decimal")
    return result


def uint(value):
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value < 2**256:
        raise ValueError("invalid uint256")
    return f"{value:064x}"


def addr_word(value):
    return address(value)[2:].rjust(64, "0")


def raw(value, decimals):
    amount = number(value) * 10**decimals
    if amount != amount.to_integral_value():
        raise ValueError("amount exceeds token precision")
    return int(amount)


def checksum(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def quote_data(amount, path):
    return "0x" + SELECTORS["quote"] + uint(amount) + uint(64) + uint(len(path)) + "".join(addr_word(a) for a in path)


def decode_quote(value, expected_length):
    if not isinstance(value, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", value):
        raise ValueError("invalid router quote")
    data = value[2:]
    if len(data) != (2 + expected_length) * 64:
        raise ValueError("invalid quote length")
    words = [int(data[i:i+64], 16) for i in range(0, len(data), 64)]
    if words[:2] != [32, expected_length] or any(v <= 0 for v in words[2:]):
        raise ValueError("invalid quote shape or empty pool")
    return words[2:]


class RPC:
    """Public reads only; no signing method, key loader or broadcast method."""
    ALLOWED = {"eth_chainId", "eth_blockNumber", "eth_getBlockByNumber", "eth_getCode",
               "eth_call", "eth_estimateGas", "eth_gasPrice", "eth_getBalance",
               "eth_getTransactionByHash", "eth_getTransactionReceipt"}

    def __init__(self, url):
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("public HTTPS RPC required")
        self.url = url

    def __call__(self, method, params):
        if method not in self.ALLOWED:
            raise ValueError("RPC method denied")
        request = Request(self.url, json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
                          {"Content-Type": "application/json"})
        with urlopen(request, timeout=20) as response:
            data = json.load(response)
        if "error" in data or "result" not in data:
            raise ValueError("RPC read or simulation failed")
        return data["result"]


def validate_policy(policy):
    allowed = {"chain_id", "wallet", "router", "settlement", "asset", "code_sha256",
               "target_asset_bps", "drift_bps", "max_trade_settlement", "slippage_bps",
               "max_price_impact_bps", "max_gas_bnb", "ttl_seconds", "mode"}
    if set(policy) != allowed or not isinstance(policy["chain_id"], int) or policy["chain_id"] != CHAIN or isinstance(policy["chain_id"], bool):
        raise ValueError("strict testnet policy required")
    if policy["mode"] != "OWNER_TARGET_TESTNET":
        raise ValueError("automatic alpha execution remains NOT LIVE READY")
    for field in ("wallet", "router", "settlement", "asset"):
        address(policy[field])
    if len({address(policy[k]) for k in ("router", "settlement", "asset")}) != 3:
        raise ValueError("contracts must differ")
    expected = {address(policy[k]) for k in ("router", "settlement", "asset")}
    pins = policy["code_sha256"]
    if not isinstance(pins, dict) or set(pins) != expected:
        raise ValueError("pin every verified contract bytecode")
    if any(not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v) for v in pins.values()):
        raise ValueError("invalid contract code hash")
    for key, low, high in (("target_asset_bps", 0, 5000), ("drift_bps", 50, 1000),
                           ("slippage_bps", 1, 100), ("max_price_impact_bps", 1, 200), ("ttl_seconds", 30, 300)):
        value = policy[key]
        if not isinstance(value, int) or isinstance(value, bool) or not low <= value <= high:
            raise ValueError("invalid bounded policy setting: " + key)
    if not 0 < number(policy["max_trade_settlement"]) <= 10 or not 0 < number(policy["max_gas_bnb"]) <= Decimal("0.001"):
        raise ValueError("testnotional or gas cap exceeded")
    return policy


def build_plan(policy, rpc, now):
    validate_policy(policy)
    if int(rpc("eth_chainId", []), 16) != CHAIN:
        raise ValueError("RPC chain mismatch")
    block = rpc("eth_blockNumber", [])
    head = rpc("eth_getBlockByNumber", [block, False])
    if not isinstance(now, int) or not 0 <= now - int(head["timestamp"], 16) <= 60:
        raise ValueError("stale or future chain head")
    wallet, router, settlement, asset = [address(policy[k]) for k in ("wallet", "router", "settlement", "asset")]
    for contract, pin in policy["code_sha256"].items():
        code = rpc("eth_getCode", [contract, block])
        if not re.fullmatch(r"0x(?:[0-9a-fA-F]{2})+", code) or hashlib.sha256(bytes.fromhex(code[2:])).hexdigest() != pin:
            raise ValueError("contract code pin mismatch")

    def call(to, data):
        return rpc("eth_call", [{"to": to, "data": data}, block])

    def decimals(token):
        value = int(call(token, "0x" + SELECTORS["decimals"]), 16)
        if not 0 <= value <= 18:
            raise ValueError("unsupported token decimals")
        return value

    def balance(token):
        return int(call(token, "0x" + SELECTORS["balance"] + addr_word(wallet)), 16)

    def quote(amount, path):
        result = decode_quote(call(router, quote_data(amount, path)), len(path))
        if result[0] != amount:
            raise ValueError("quote input mismatch")
        return result[-1]

    sd, ad = decimals(settlement), decimals(asset)
    sb, ab = balance(settlement), balance(asset)
    unit_price = quote(10**ad, [asset, settlement])
    asset_value = ab * unit_price // 10**ad
    total = sb + asset_value
    if total == 0:
        raise ValueError("empty test treasury")
    current_bps = asset_value * 10000 // total
    base = {"schema_version": 1, "chain_id": CHAIN, "wallet": wallet, "created_at": now,
            "expires_at": now + policy["ttl_seconds"], "block": block, "block_hash": head["hash"],
            "policy": policy, "policy_sha256": checksum(policy), "asset_weight_bps": current_bps,
            "status": "HOLD", "transactions": [], "executed": False, "campaign_qualified": False}
    if abs(current_bps - policy["target_asset_bps"]) < policy["drift_bps"]:
        return base
    delta = total * policy["target_asset_bps"] // 10000 - asset_value
    cap = raw(policy["max_trade_settlement"], sd)
    notional = min(abs(delta), cap)
    buying = delta > 0
    path = [settlement, asset] if buying else [asset, settlement]
    amount = min(sb, notional) if buying else min(ab, notional * 10**ad // unit_price)
    if amount <= 0:
        return base
    # Direct two-token paths only. No bridging, lending, native transfers or fee-on-transfer tokens.
    output = quote(amount, path)
    expected = amount * 10**ad // unit_price if buying else amount * unit_price // 10**ad
    if expected <= 0 or output * 10000 < expected * (10000 - policy["max_price_impact_bps"]):
        raise ValueError("quote impact exceeds policy")
    minimum = output * (10000 - policy["slippage_bps"]) // 10000
    if minimum <= 0:
        raise ValueError("empty minimum output")
    allowance = int(call(path[0], "0x" + SELECTORS["allowance"] + addr_word(wallet) + addr_word(router)), 16)
    if allowance < amount:
        approval_amount = 0 if allowance else amount
        tx = {"from": wallet, "to": path[0], "data": "0x" + SELECTORS["approve"] + addr_word(router) + uint(approval_amount), "value": "0x0"}
        status = "APPROVE_THEN_REPLAN"  # Rebuild after each receipt; never queue an unsimulated swap.
    else:
        tx = {"from": wallet, "to": router,
              "data": "0x" + SELECTORS["swap"] + uint(amount) + uint(minimum) + uint(160) + addr_word(wallet)
                      + uint(base["expires_at"]) + uint(2) + "".join(addr_word(a) for a in path), "value": "0x0"}
        status = "SWAP_REQUIRES_WALLET_SIGNATURE"
    rpc("eth_call", [tx, "latest"])  # Refuse reverted allowance/swap; approvals are not counted as execution.
    gas = int(rpc("eth_estimateGas", [tx]), 16)
    gas_price = int(rpc("eth_gasPrice", []), 16)
    if gas <= 0 or gas_price <= 0:
        raise ValueError("invalid gas estimate")
    gas_limit = (gas * 120 + 99) // 100
    cost = gas_limit * gas_price
    if cost > raw(policy["max_gas_bnb"], 18) or cost > int(rpc("eth_getBalance", [wallet, "latest"]), 16):
        raise ValueError("gas cap or balance insufficient")
    tx.update(gas=hex(gas_limit), gasPrice=hex(gas_price))
    base.update(status=status, side="buy" if buying else "sell", amount_in=str(amount), min_amount_out=str(minimum),
                path=path, max_gas_wei=str(raw(policy["max_gas_bnb"], 18)), transactions=[tx])
    base["plan_sha256"] = checksum(base)
    return base


def verify_receipt(plan, tx_hash, rpc):
    """Verify one real receipt. Does not label a transfer/approval as a rebalance."""
    if not isinstance(tx_hash, str) or not re.fullmatch(r"0x[0-9a-fA-F]{64}", tx_hash):
        raise ValueError("invalid transaction hash")
    candidate = dict(plan)
    digest = candidate.pop("plan_sha256", None)
    if digest != checksum(candidate) or len(plan["transactions"]) != 1:
        raise ValueError("plan changed")
    validate_policy(plan["policy"])
    if plan["chain_id"] != CHAIN or int(rpc("eth_chainId", []), 16) != CHAIN:
        raise ValueError("receipt chain mismatch")
    tx = rpc("eth_getTransactionByHash", [tx_hash])
    receipt = rpc("eth_getTransactionReceipt", [tx_hash])
    if not tx or not receipt:
        raise ValueError("transaction not yet confirmed")
    expected = plan["transactions"][0]
    if address(tx["from"]) != address(plan["wallet"]) or address(tx["to"]) != address(expected["to"]) or tx["input"].lower() != expected["data"].lower() or int(tx["value"], 16) != 0:
        raise ValueError("receipt does not match reviewed transaction")
    if receipt["transactionHash"].lower() != tx_hash.lower() or int(receipt["status"], 16) != 1:
        raise ValueError("transaction reverted")
    head = rpc("eth_getBlockByNumber", [receipt["blockNumber"], False])
    if not head or head["hash"].lower() != receipt["blockHash"].lower():
        raise ValueError("receipt block no longer canonical")
    if int(head["timestamp"], 16) > plan["expires_at"]:
        raise ValueError("receipt after plan expiry")
    gas_cost = int(receipt["gasUsed"], 16) * int(receipt["effectiveGasPrice"], 16)
    if gas_cost > int(plan["max_gas_wei"]):
        raise ValueError("actual gas exceeded reviewed cap")
    return {"chain_id": CHAIN, "tx_hash": tx_hash.lower(), "block_number": int(receipt["blockNumber"], 16),
            "timestamp": int(head["timestamp"], 16), "wallet": plan["wallet"], "plan_sha256": digest,
            "kind": "DEX_SWAP" if plan["status"] == "SWAP_REQUIRES_WALLET_SIGNATURE" else "TOKEN_APPROVAL",
            "campaign_qualified": False, "note": "Receipt confirms call success; identity attribution, swap outcome and campaign review are separate."}
