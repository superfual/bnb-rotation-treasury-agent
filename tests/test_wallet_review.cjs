// Pure VM tests against an injected fake provider, never a browser or real wallet.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const {webcrypto}=require('node:crypto'),{execFileSync}=require('node:child_process');
const code=fs.readFileSync('docs/testnet-wallet-review.html','utf8').split('<script>')[1].split('</script>')[0];
const fixture=JSON.parse(execFileSync('python',['-c',"import json;from test_onchain import FakeRPC,policy;from bnb_rotation.onchain import build_plan;print(json.dumps(build_plan(policy(),FakeRPC(),1000)))"],{env:{...process.env,PYTHONPATH:'src:tests'},encoding:'utf8'}));
const word=x=>BigInt(x).toString(16).padStart(64,'0');
async function trial(p,chain=97){
 const elements=Object.fromEntries(['file','view','sign','result'].map(k=>[k,{disabled:true,textContent:''}]));let sent=0;
 const provider={request:async({method,params=[]})=>{
  if(method==='eth_chainId')return '0x'+chain.toString(16);
  if(method==='eth_requestAccounts')return [fixture.wallet];
  if(method==='eth_getCode')return '0x60016000';
  if(method==='eth_estimateGas')return '0x186a0';
  if(method==='eth_gasPrice')return '0x5f5e100';
  if(method==='eth_getBalance')return '0x'+word(10n**18n);
  if(method==='eth_sendTransaction'){sent++;return '0x'+'b'.repeat(64);}
  if(method==='eth_call'){
   const tx=params[0],s=tx.data.slice(2,10);
   if(s==='313ce567')return '0x'+word(18);
   if(s==='70a08231')return '0x'+word(tx.to===fixture.policy.settlement?100n*10n**18n:0);
   if(s==='d06ca61f'){const n=BigInt('0x'+tx.data.slice(10,74));return '0x'+word(32)+word(2)+word(n)+word(n*2n);}
   return '0x';
  }
  throw Error('Unexpected RPC '+method);
 }};
 const context={document:{getElementById:k=>elements[k]},window:{ethereum:provider},crypto:webcrypto,TextEncoder,
                Date:class extends Date{static now(){return 1000000;}}};
 vm.createContext(context);vm.runInContext(code,context);
 await elements.file.onchange({target:{files:[{text:async()=>JSON.stringify(p)}]}});
 if(!elements.sign.disabled)await elements.sign.onclick();
 return {sent,elements};
}
(async()=>{
 assert.equal((await trial(fixture)).sent,1,'valid testnet approval requests exactly one wallet signature');
 assert.equal((await trial(fixture,56)).sent,0,'mainnet provider is blocked');
 const modified=structuredClone(fixture);modified.transactions[0].value='0x1';assert.equal((await trial(modified)).sent,0,'modified plan blocked');
 const expired=structuredClone(fixture);expired.expires_at=999;assert.equal((await trial(expired)).sent,0,'expired plan blocked');
 console.log('4 browser-review VM checks passed (fake provider only).');
})().catch(e=>{console.error(e);process.exitCode=1;});
