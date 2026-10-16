const assert=require('node:assert/strict');
global.crypto=require('node:crypto').webcrypto;
const A=require('../dist/evidence.js'),E=require('../dist/engine.js');
const word=n=>BigInt(n).toString(16).padStart(64,'0');
function uri(s){const b=Buffer.from(s);return '0x'+word(32)+word(b.length)+b.toString('hex').padEnd(Math.ceil(b.length/32)*64,'0');}
function reader({chain=56,owner=A.identity.owner,registration=A.identity.registrationURI,age=0}={}){return async items=>items.map(([m,p])=>{if(m==='eth_chainId')return '0x'+chain.toString(16);if(m==='eth_blockNumber')return '0x100';if(m==='eth_getBlockByNumber')return {timestamp:'0x'+(Math.floor(Date.now()/1000)-age).toString(16),hash:'0x'+'a'.repeat(64)};assert.equal(p[0].to,A.identity.registry);assert.equal(p[1],'0x100');return p[0].data.startsWith('0x6352211e')?'0x'+owner.slice(2).padStart(64,'0'):uri(registration);});}
function storage(){const map=new Map();return {map,getItem:k=>map.get(k)??null,setItem:(k,v)=>map.set(k,v)};}
(async()=>{
 const binding=await A.checkIdentity(reader());assert.equal(binding.agentId,370316);
 await assert.rejects(()=>A.checkIdentity(reader({chain:97})),/Sai mạng/);
 await assert.rejects(()=>A.checkIdentity(reader({owner:E.C.asset})),/Chủ sở hữu/);
 await assert.rejects(()=>A.checkIdentity(reader({registration:'https://example.com/replaced'})),/URI/);
 await assert.rejects(()=>A.checkIdentity(reader({age:90})),/đã cũ/);
 const plan={kind:'HOLD',snapshot:{cash:7n,asset:3n},reason:'target'},proof=await A.seal(plan,binding,E.C);
 await A.verifySeal(plan,proof);await assert.rejects(()=>A.verifySeal({...plan,kind:'SWAP'},proof),/đã thay đổi/);
 const store=storage();await A.append(store,'decision-1','DECISION',{proof,plan});await A.append(store,'receipt-1','CONFIRMED',{hash:'0x'+'b'.repeat(64)});assert.equal((await A.readJournal(store)).entries.length,2);
 await A.append(store,'receipt-1','CONFIRMED',{hash:'0x'+'b'.repeat(64)});assert.equal((await A.readJournal(store)).entries.length,2);
 await assert.rejects(()=>A.append(store,'receipt-1','CONFIRMED',{hash:'0x'+'c'.repeat(64)}),/khác nội dung/);
 const corrupted=JSON.parse(store.getItem(A.journalKey));corrupted.entries[0].data.plan.kind='SWAP';store.setItem(A.journalKey,JSON.stringify(corrupted));await assert.rejects(()=>A.readJournal(store),/đã thay đổi/);
 await assert.rejects(()=>A.append({getItem:()=>null,setItem:()=>{throw Error('quota full');}},'decision','DECISION',{plan}),/quota full/);
 console.log('Identity, URI, freshness, plan tampering, journal integrity, deduplication and storage failure checks passed.');
})().catch(e=>{console.error(e);process.exitCode=1;});
