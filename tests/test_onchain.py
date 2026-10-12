import copy
import hashlib
import unittest

from bnb_rotation.onchain import (build_plan, checksum, decode_quote, quote_data,
                                  raw, uint, validate_policy, verify_receipt)

W, R, S, A = ['0x'+x*40 for x in '1234']
CODE = '0x60016000'
PIN = hashlib.sha256(bytes.fromhex(CODE[2:])).hexdigest()


def policy():
    return {'chain_id':97,'mode':'OWNER_TARGET_TESTNET','wallet':W,'router':R,'settlement':S,'asset':A,
            'code_sha256':{R:PIN,S:PIN,A:PIN},'target_asset_bps':3000,'drift_bps':500,
            'max_trade_settlement':'1','slippage_bps':50,'max_price_impact_bps':100,
            'max_gas_bnb':'0.0001','ttl_seconds':180}


class FakeRPC:
    def __init__(self):
        self.chain=97;self.allowance=0;self.asset=0;self.cash=100*10**18
        self.revert=False;self.impact=False;self.stale=False;self.code=CODE
        self.tx=None;self.receipt=None;self.calls=[]

    def __call__(self, method, params):
        self.calls.append(method)
        if method=='eth_chainId':return hex(self.chain)
        if method=='eth_blockNumber':return '0x10'
        if method=='eth_getBlockByNumber':return {'timestamp':hex(900 if self.stale else 1000),'hash':'0x'+'a'*64}
        if method=='eth_getCode':return self.code
        if method=='eth_estimateGas':return hex(100000)
        if method=='eth_gasPrice':return hex(100000000)
        if method=='eth_getBalance':return hex(10**18)
        if method=='eth_getTransactionByHash':return self.tx
        if method=='eth_getTransactionReceipt':return self.receipt
        if method=='eth_call':
            tx=params[0];data=tx['data'];selector=data[2:10]
            if selector=='313ce567':return '0x'+uint(18)
            if selector=='70a08231':return '0x'+uint(self.cash if tx['to']==S else self.asset)
            if selector=='dd62ed3e':return '0x'+uint(self.allowance)
            if selector=='d06ca61f':
                amount=int(data[10:74],16);first='0x'+data[202:266][-40:]
                output=amount*2 if first==A else amount//2
                if self.impact and first==S:output//=2
                return '0x'+uint(32)+uint(2)+uint(amount)+uint(output)
            if self.revert:raise ValueError('simulation reverted')
            return '0x'
        raise AssertionError(method)


class OnchainTests(unittest.TestCase):
    def test_mainnet_automatic_mode_and_unknown_fields_denied(self):
        for field,value in [('chain_id',56),('mode','AUTO_ALPHA'),('extra',True),('target_asset_bps',5001),('slippage_bps',101),('max_trade_settlement','11')]:
            p=policy();p[field]=value
            with self.assertRaises(ValueError):validate_policy(p)

    def test_precision_and_nonfinite_inputs_rejected(self):
        for v in ['NaN','Infinity','-1',True,0.5]:
            with self.assertRaises(ValueError):raw(v,18)
        with self.assertRaises(ValueError):raw('0.0000001',6)
        self.assertEqual(raw('1.25',6),1250000)

    def test_abi_quote_dynamic_array_roundtrip_and_malformed(self):
        data=quote_data(123,[S,A]);self.assertEqual(len(data),330)
        q='0x'+uint(32)+uint(2)+uint(123)+uint(456)
        self.assertEqual(decode_quote(q,2),[123,456])
        for bad in ['0x',q[:-2],'0x'+uint(64)+q[66:],'0x'+uint(32)+uint(2)+uint(0)+uint(1)]:
            with self.assertRaises(ValueError):decode_quote(bad,2)

    def test_first_plan_only_approves_exact_amount_no_swap_or_broadcast(self):
        rpc=FakeRPC();p=build_plan(policy(),rpc,1000)
        self.assertEqual(p['status'],'APPROVE_THEN_REPLAN')
        self.assertEqual(int(p['transactions'][0]['data'][-64:],16),10**18)
        self.assertEqual(p['transactions'][0]['to'],S)
        self.assertFalse(p['executed']);self.assertFalse(p['campaign_qualified'])
        self.assertNotIn('eth_sendTransaction',rpc.calls)

    def test_nonzero_insufficient_allowance_resets_before_new_plan(self):
        rpc=FakeRPC();rpc.allowance=1;p=build_plan(policy(),rpc,1000)
        self.assertEqual(int(p['transactions'][0]['data'][-64:],16),0)

    def test_swap_binds_recipient_deadline_path_slippage_and_cap(self):
        rpc=FakeRPC();rpc.allowance=10**18;p=build_plan(policy(),rpc,1000);d=p['transactions'][0]['data']
        self.assertEqual(p['status'],'SWAP_REQUIRES_WALLET_SIGNATURE')
        self.assertEqual(int(d[10:74],16),10**18)
        self.assertEqual(int(d[74:138],16),497500000000000000)
        self.assertEqual('0x'+d[202:266][-40:],W)
        self.assertEqual(int(d[266:330],16),1180)
        self.assertEqual(p['path'],[S,A]);self.assertEqual(p['transactions'][0]['value'],'0x0')

    def test_sell_plan_and_in_band_hold_do_not_churn(self):
        rpc=FakeRPC();rpc.asset=50*10**18;rpc.cash=0;rpc.allowance=10**18
        self.assertEqual(build_plan(policy(),rpc,1000)['side'],'sell')
        rpc.asset=15*10**18;rpc.cash=70*10**18
        p=build_plan(policy(),rpc,1000);self.assertEqual(p['status'],'HOLD');self.assertEqual(p['transactions'],[])

    def test_wrong_chain_stale_head_code_revert_and_quote_impact_block(self):
        for attr,value in [('chain',56),('stale',True),('code','0x6002'),('revert',True),('impact',True)]:
            rpc=FakeRPC();setattr(rpc,attr,value)
            with self.subTest(attr=attr),self.assertRaises(ValueError):build_plan(policy(),rpc,1000)

    def test_gas_budget_and_empty_wallet_fail(self):
        p=policy();p['max_gas_bnb']='0.00000001'
        with self.assertRaises(ValueError):build_plan(p,FakeRPC(),1000)
        rpc=FakeRPC();rpc.cash=0
        with self.assertRaises(ValueError):build_plan(policy(),rpc,1000)

    def test_receipt_pending_reverted_tampered_and_foreign_transactions_rejected(self):
        rpc=FakeRPC();rpc.allowance=10**18;p=build_plan(policy(),rpc,1000);h='0x'+'b'*64
        with self.assertRaises(ValueError):verify_receipt(p,h,rpc)
        tx=p['transactions'][0];rpc.tx={'from':W,'to':R,'input':tx['data'],'value':'0x0'}
        rpc.receipt={'transactionHash':h,'status':'0x1','blockNumber':'0x10','blockHash':'0x'+'a'*64,'gasUsed':hex(100000),'effectiveGasPrice':hex(100000000)}
        evidence=verify_receipt(p,h,rpc);self.assertEqual(evidence['kind'],'DEX_SWAP');self.assertFalse(evidence['campaign_qualified'])
        rpc.receipt['status']='0x0'
        with self.assertRaises(ValueError):verify_receipt(p,h,rpc)
        rpc.receipt['status']='0x1';rpc.tx['from']=S
        with self.assertRaises(ValueError):verify_receipt(p,h,rpc)
        changed=copy.deepcopy(p);changed['wallet']=S
        with self.assertRaises(ValueError):verify_receipt(changed,h,rpc)

    def test_approval_receipt_is_never_rebalance_evidence(self):
        rpc=FakeRPC();p=build_plan(policy(),rpc,1000);h='0x'+'b'*64;tx=p['transactions'][0]
        rpc.tx={'from':W,'to':S,'input':tx['data'],'value':'0x0'}
        rpc.receipt={'transactionHash':h,'status':'0x1','blockNumber':'0x10','blockHash':'0x'+'a'*64,'gasUsed':hex(100000),'effectiveGasPrice':hex(100000000)}
        self.assertEqual(verify_receipt(p,h,rpc)['kind'],'TOKEN_APPROVAL')


if __name__=='__main__':unittest.main()
