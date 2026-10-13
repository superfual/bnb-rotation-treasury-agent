const assert=require('node:assert/strict'),fs=require('node:fs');
global.crypto=require('node:crypto').webcrypto;
const E=require('../dist/engine.js'),C=E.C,W=E.word,A=E.aw,codes=JSON.parse(fs.readFileSync('tests/runtime-code.json','utf8'));let count=0;
function fixture(){
 const x={chain:97,cash:9n*10n**18n,asset:0n,ar:10n**18n,sr:200n*10n**18n,allowance:0n,price:100000000n,native:10n**17n,badCode:false,badPair:false,revert:false,tx:null,receipt:null,reorg:false};
 const quote=(n,path)=>{const buy=path[0]===C.cash,rin=buy?x.sr:x.ar,rout=buy?x.ar:x.sr;return n*9975n*rout/(rin*10000n+n*9975n);};
 const array=(n,out)=>'0x'+W(32)+W(2)+W(n)+W(out);
 x.read=async items=>items.map(([method,p])=>{
  if(method==='eth_chainId')return '0x'+x.chain.toString(16);
  if(method==='eth_blockNumber')return '0x103';
  if(method==='eth_getBlockByNumber')return {timestamp:'0x'+Math.floor(Date.now()/1000).toString(16),hash:'0x'+(x.reorg?'b':'a').repeat(64)};
  if(method==='eth_getCode')return x.badCode?'0x6000':codes[p[0]];
  if(method==='eth_estimateGas')return '0x186a0';
  if(method==='eth_gasPrice')return '0x'+x.price.toString(16);
  if(method==='eth_getBalance')return '0x'+x.native.toString(16);
  if(method==='eth_getTransactionByHash')return x.tx;
  if(method==='eth_getTransactionReceipt')return x.receipt;
  if(method==='eth_call'){
   const tx=p[0],data=tx.data,s=data.slice(2,10);
   if(s==='c45a0155')return '0x'+A(C.factory);
   if(s==='e6a43905')return '0x'+A(x.badPair?C.wallet:C.pair);
   if(s==='0dfe1681')return '0x'+A(C.asset);
   if(s==='d21220a7')return '0x'+A(C.cash);
   if(s==='0902f1ac')return '0x'+W(x.ar)+W(x.sr)+W(Math.floor(Date.now()/1000));
   if(s==='313ce567')return '0x'+W(18);
   if(s==='70a08231')return '0x'+W(tx.to===C.cash?x.cash:x.asset);
   if(s==='dd62ed3e')return '0x'+W(x.allowance);
   if(s==='d06ca61f'){const n=BigInt('0x'+data.slice(10,74)),first='0x'+data.slice(202,266).slice(-40);return array(n,quote(n,[first]));}
   if(x.revert)throw Error('revert');
   if(s==='095ea7b3')return '0x'+W(1);
   if(s==='38ed1739'){const n=BigInt('0x'+data.slice(10,74)),first='0x'+data.slice(394,458).slice(-40);return array(n,quote(n,[first]));}
  }
  throw Error('Unexpected method '+method);
 });
 return x;
}
async function test(name,f){await f();count++;console.log('PASS '+name);}
function receipt(x,p){const h='0x'+'c'.repeat(64),topic='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef';x.tx={from:C.wallet,to:p.tx.to,input:p.tx.data,value:'0x0'};x.receipt={transactionHash:h,status:'0x1',blockNumber:'0x100',blockHash:'0x'+'a'.repeat(64),gasUsed:'0x186a0',effectiveGasPrice:'0x5f5e100',logs:[{address:C.cash,topics:[topic,'0x'+A(C.wallet),'0x'+A(C.pair)],data:'0x'+W(p.amount)},{address:C.asset,topics:[topic,'0x'+A(C.pair),'0x'+A(C.wallet)],data:'0x'+W(p.out)}]};return h;}
(async()=>{
 await test('real pinned contract bytecode is verified',async()=>{const s=await E.snapshot(fixture().read);assert.equal(s.cash,9n*10n**18n);});
 await test('mainnet read is blocked',async()=>{const x=fixture();x.chain=56;await assert.rejects(()=>E.prepare(x.read),/Sai mạng/);});
 await test('changed code and wrong pool are blocked',async()=>{let x=fixture();x.badCode=true;await assert.rejects(()=>E.prepare(x.read));x=fixture();x.badPair=true;await assert.rejects(()=>E.prepare(x.read));});
 await test('first transaction approves exact one U, never unlimited',async()=>{const p=await E.prepare(fixture().read);assert.equal(p.kind,'APPROVE');assert.equal(p.approvalAmount,C.cap);assert.equal(BigInt('0x'+p.tx.data.slice(-64)),C.cap);E.assertPlan(p);});
 await test('partial allowance generates only zero reset',async()=>{const x=fixture();x.allowance=1n;const p=await E.prepare(x.read);assert.equal(p.approvalAmount,0n);});
 await test('swap binds exact amount, owner, deadline and non-native path',async()=>{const x=fixture();x.allowance=C.cap;const p=await E.prepare(x.read);assert.equal(p.kind,'SWAP');assert.equal(p.amount,C.cap);assert.equal(p.tx.value,'0x0');assert.equal(p.expires-p.created,300);E.assertPlan(p);assert.ok(p.minimum>0n);});
 await test('in-band allocation holds without transaction',async()=>{const x=fixture();x.cash=7n*10n**18n;x.asset=15n*10n**15n;const p=await E.prepare(x.read);assert.equal(p.kind,'HOLD');});
 await test('excess pool impact and gas are blocked',async()=>{let x=fixture();x.ar=10n**16n;x.sr=2n*10n**18n;await assert.rejects(()=>E.prepare(x.read),/tác động giá/);x=fixture();x.price=10n**12n;await assert.rejects(()=>E.prepare(x.read),/Phí vượt/);});
 await test('tampered recipient or expired plan cannot reach signing',async()=>{const p=await E.prepare(fixture().read);p.tx.to=C.wallet;assert.throws(()=>E.assertPlan(p));const fresh=await E.prepare(fixture().read);fresh.created-=301;fresh.expires-=301;assert.throws(()=>E.assertPlan(fresh));});
 await test('adverse price change blocks the original reviewed swap',async()=>{const x=fixture();x.allowance=C.cap;const p=await E.prepare(x.read);x.ar=x.ar*80n/100n;await assert.rejects(()=>E.validateForSend(p,x.read),/giá đã đổi/);});
 await test('successful receipt reconciles actual transfer amounts',async()=>{const x=fixture();x.allowance=C.cap;const p=await E.prepare(x.read),h=receipt(x,p);const proof=await E.verify(p,h,x.read);assert.equal(proof.pending,false);assert.equal(proof.input,C.cap);assert.equal(proof.output,p.out);assert.equal(proof.campaignQualified,false);});
 await test('reverted, foreign and reorged receipts are rejected',async()=>{const x=fixture();x.allowance=C.cap;const p=await E.prepare(x.read),h=receipt(x,p);x.receipt.status='0x0';await assert.rejects(()=>E.verify(p,h,x.read));x.receipt.status='0x1';x.tx.from=C.asset;await assert.rejects(()=>E.verify(p,h,x.read));x.tx.from=C.wallet;x.reorg=true;await assert.rejects(()=>E.verify(p,h,x.read));});
 await test('insufficient actual output is rejected',async()=>{const x=fixture();x.allowance=C.cap;const p=await E.prepare(x.read),h=receipt(x,p);x.receipt.logs[1].data='0x'+W(p.minimum-1n);await assert.rejects(()=>E.verify(p,h,x.read),/thực nhận/);});
 await test('pending receipt stays pending and exact approval remains separate',async()=>{const x=fixture(),p=await E.prepare(x.read);assert.equal((await E.verify(p,'0x'+'c'.repeat(64),x.read)).pending,true);const h=receipt(x,p);x.allowance=p.approvalAmount;const proof=await E.verify(p,h,x.read);assert.equal(proof.kind,'APPROVE');assert.equal(proof.output,0n);});
 await test('malformed batch response and write RPC methods are rejected',async()=>{await assert.rejects(()=>E.batch([['eth_sendTransaction',[]]],async()=>{}));await assert.rejects(()=>E.batch([['eth_chainId',[]],['eth_blockNumber',[]]],async()=>({ok:true,json:async()=>[{id:0,result:'0x61'},{id:0,result:'0x10'}]})));});
 await test('pending persistence preserves exact integer amounts',async()=>{const p=await E.prepare(fixture().read);assert.equal(E.unpack(E.pack(p)).amount,p.amount);});
 console.log(count+' engine checks passed. No real signing or broadcast performed.');
})().catch(e=>{console.error(e);process.exitCode=1;});
