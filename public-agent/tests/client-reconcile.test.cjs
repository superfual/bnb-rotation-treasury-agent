global.crypto=require('node:crypto').webcrypto;
const assert=require('node:assert/strict'),A=require('../client-ui/evidence.js'),factory=require('../client-ui/engine.js'),{verifyJournals}=require('../scripts/verify-client-journal.cjs');
const E=factory.createForWallet('0x1111111111111111111111111111111111111111'),now=Math.floor(Date.now()/1000),hash='0x'+'c'.repeat(64);
function store(){let raw=null;return {getItem:()=>raw,setItem:(_,x)=>{raw=x;}};}
const binding={...A.identity,checkedAt:new Date().toISOString()};
async function journal({hold=false,confirmedFirst=false}={}){
 const st=store(),plan=hold?{kind:'HOLD',snapshot:{weight:3000}}:{kind:'SWAP',buy:true,amount:E.C.cap,minimum:1n,path:[E.C.cash,E.C.asset],created:now,expires:now+300,tx:{from:E.C.wallet,to:E.C.router,value:'0x0',data:'0x38ed1739'+E.word(E.C.cap)+E.word(1)+E.word(160)+E.aw(E.C.wallet)+E.word(now+300)+E.word(2)+[E.C.cash,E.C.asset].map(E.aw).join('')}};
 const proof=await A.seal(plan,binding,E.C);
 const confirmed=()=>A.append(st,'confirmed','CONFIRMED',{proof,hash,kind:'SWAP'});
 if(confirmedFirst)await confirmed();
 await A.append(st,'plan',hold?'DECISION':'SIGN_REQUESTED',{proof,plan});
 if(!hold&&!confirmedFirst)await confirmed();
 return st.getItem();
}
(async()=>{
 let calls=0;const deps={verify:async()=>{calls++;return {pending:false,block:123,input:E.C.cap,output:1n,fee:1n};},readBlock:async()=>({timestamp:'0x'+(now+1).toString(16)})};
 const hold=await verifyJournals([await journal({hold:true})],deps);assert.equal(hold.candidateSwapCount,0);assert.equal(calls,0);
 const raw=await journal(),good=await verifyJournals([raw,raw],deps);assert.equal(good.candidateSwapCount,1);assert.equal(good.verifiedReceipts.length,1);assert.equal(calls,1);
 await assert.rejects(()=>verifyJournals([raw],{...deps,verify:async()=>{throw Error('reverted');}}),/reverted/);
 await assert.rejects(()=>verifyJournals([raw],{...deps,verify:async()=>({pending:true})}),/pending/);
 const unordered=await journal({confirmedFirst:true});await assert.rejects(()=>verifyJournals([unordered],deps),/preceding/);
 const corrupt=JSON.parse(raw);corrupt.entries[0].data.plan.tx.to=E.C.wallet;await assert.rejects(()=>verifyJournals([JSON.stringify(corrupt)],deps),/đã thay đổi/);
 assert.equal(good.broadcastsPerformed,0);assert.match(good.campaignQualification,/unconfirmed/);
 console.log('Reconciliation: HOLD excluded, duplicate receipt deduplicated, pending/revert/tamper/out-of-order rejected; no broadcast');
})().catch(e=>{console.error(e);process.exitCode=1;});
