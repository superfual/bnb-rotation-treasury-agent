'use strict';
global.crypto??=require('node:crypto').webcrypto;
const fs=require('node:fs/promises'),A=require('../client-ui/evidence.js'),factory=require('../client-ui/engine.js');
function retainedCall(p,E){
 if(!p||!['SWAP','APPROVE'].includes(p.kind)||p.amount<=0n||p.minimum<=0n||p.expires-p.created!==E.C.ttl)throw Error('Invalid retained plan');
 const path=p.buy?[E.C.cash,E.C.asset]:[E.C.asset,E.C.cash];
 if(p.path?.join(',')!==path.join(','))throw Error('Unexpected retained token path');
 const expected=p.kind==='SWAP'?'0x38ed1739'+E.word(p.amount)+E.word(p.minimum)+E.word(160)+E.aw(E.C.wallet)+E.word(p.expires)+E.word(2)+path.map(E.aw).join(''):'0x095ea7b3'+E.aw(E.C.router)+E.word(p.approvalAmount);
 if(E.addr(p.tx.from)!==E.C.wallet||E.addr(p.tx.to)!==(p.kind==='SWAP'?E.C.router:path[0])||BigInt(p.tx.value)!==0n||p.tx.data.toLowerCase()!==expected.toLowerCase()||p.kind==='APPROVE'&&p.approvalAmount!==0n&&p.approvalAmount!==p.amount)throw Error('Retained calldata differs from fixed policy');
}
async function verifyJournals(raws,dependencies={}){
 const confirmed=new Map(),decisions=[];
 for(const raw of raws){
  const journal=await A.readJournal({getItem:()=>raw}),plans=new Map();
  for(const entry of journal.entries){
   if(!['DECISION','SIGN_REQUESTED'].includes(entry.event))continue;
   const {proof,plan}=factory.unpack(JSON.stringify(entry.data));
   if(!proof||!plan)throw Error('Missing retained plan/proof');
   await A.verifySeal(plan,proof);
   const E=factory.createForWallet(proof.policy.wallet);
   if(await A.digest(proof.policy)!==await A.digest(E.C)||proof.binding.chainId!==56||proof.binding.executionChainId!==97||proof.binding.registry!==A.identity.registry)throw Error('Unsupported identity or execution policy');
   decisions.push({kind:plan.kind,planHash:proof.planHash,executor:E.C.wallet});
   if(entry.event==='SIGN_REQUESTED'){retainedCall(plan,E);plans.set(proof.planHash,{plan,proof,E,index:journal.entries.indexOf(entry),signTime:entry.at});}
  }
  for(const entry of journal.entries){
   if(entry.event!=='CONFIRMED')continue;
   const data=factory.unpack(JSON.stringify(entry.data));
   if(data.legacyUnbound||!data.proof)throw Error('Unbound legacy receipt requires separate review');
   const match=plans.get(data.proof.planHash);if(!match||match.index>=journal.entries.indexOf(entry))throw Error('Receipt has no preceding sign plan');if(await A.digest(data.proof)!==await A.digest(match.proof))throw Error('Receipt proof differs from sign plan');
   if(!/^0x[0-9a-f]{64}$/i.test(data.hash))throw Error('Invalid receipt hash');
   const {plan,E}=match;
   if(data.kind!==plan.kind)throw Error('Receipt kind differs from reviewed plan');
   if(confirmed.has(data.hash.toLowerCase())){if(confirmed.get(data.hash.toLowerCase()).planHash!==data.proof.planHash)throw Error('Conflicting plans for one transaction');continue;}
   const receipt=await (dependencies.verify??((E,p,h)=>E.verify(p,h)))(E,plan,data.hash);
   if(receipt.pending)throw Error('Receipt is still pending');
   const block=await (dependencies.readBlock??(async(E,n)=>(await E.batch([['eth_getBlockByNumber',['0x'+n.toString(16),false]]]))[0]))(E,receipt.block);
   if(!block?.timestamp)throw Error('Missing confirmed block timestamp');
   const stamp=Number(BigInt(block.timestamp));if(!Number.isSafeInteger(stamp)||stamp<plan.created||stamp>plan.expires||!Number.isFinite(Date.parse(match.signTime))||stamp<Math.floor(Date.parse(match.signTime)/1000))throw Error('Receipt outside retained plan window');
   const at=new Date(stamp*1000),dateUTC=at.toISOString().slice(0,10),dateVietnam=new Date((stamp+7*3600)*1000).toISOString().slice(0,10);
   confirmed.set(data.hash.toLowerCase(),{hash:data.hash,kind:plan.kind,executor:E.C.wallet,identityAgentId:370316,executionChainId:97,block:receipt.block,at:at.toISOString(),dateUTC,dateVietnam,planHash:data.proof.planHash,rawInput:String(receipt.input??0),rawOutput:String(receipt.output??0),rawFee:String(receipt.fee??0),withinCampaignWindow:stamp>=Date.parse('2026-10-01T00:00:00Z')/1000&&stamp<=Date.parse('2026-11-05T12:00:00Z')/1000,campaignQualification:null});
  }
 }
 const receipts=[...confirmed.values()],swaps=receipts.filter(x=>x.kind==='SWAP'&&x.withinCampaignWindow);
 return {checkedAt:new Date().toISOString(),decisions:decisions.length,holdDecisions:decisions.filter(x=>x.kind==='HOLD').length,verifiedReceipts:receipts,candidateSwapCount:swaps.length,distinctDatesUTC:[...new Set(swaps.map(x=>x.dateUTC))].sort(),distinctDatesVietnam:[...new Set(swaps.map(x=>x.dateVietnam))].sort(),requirements:{actions:5,separateDays:3},campaignQualification:'unconfirmed; local hashes are not independent attribution, and funding independence/category fit need separate evidence',broadcastsPerformed:0};
}
module.exports={verifyJournals,retainedCall};
if(require.main===module)(async()=>{const paths=process.argv.slice(2);if(!paths.length)throw Error('Provide one or more exported client journal JSON files');const raws=[];for(const path of paths){const raw=await fs.readFile(path,'utf8');if(Buffer.byteLength(raw)>2000000)throw Error('Journal exceeds 2 MB');raws.push(raw);}console.log(JSON.stringify(await verifyJournals(raws),null,2));})().catch(e=>{console.error(e.message);process.exitCode=1;});
