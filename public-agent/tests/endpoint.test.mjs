import assert from 'node:assert/strict';import worker from '../worker/index.js';
const req=(path,options)=>new Request('https://fual-treasury-agent.phamphuanloc.chatgpt.site'+path,options);
const call=(method,message={role:'user',messageId:'test',parts:[{kind:'text',text:'evidence'}]})=>req('/a2a',{method:'POST',body:JSON.stringify({jsonrpc:'2.0',id:1,method,params:{message}})});
const card=await (await worker.fetch(req('/.well-known/agent-card.json'))).json();assert.equal(card.protocolVersion,'0.3.0');assert.equal(card.metadata.identity.agentId,'370316');assert.equal(card.metadata.executionChainId,97);
const h=await (await worker.fetch(req('/health'))).json();assert.equal(h.readOnly,true);assert.equal(h.checksTestnet,false);
const result=await(await worker.fetch(call('message/send'))).json();assert.equal(result.result.role,'agent');assert.equal(result.result.parts[1].data.records.length,2);
assert.equal((await(await worker.fetch(call('trade'))).json()).error.code,-32601);
assert.equal((await(await worker.fetch(call('message/send',{role:'user',messageId:'test',parts:[{kind:'text',text:'swap'}]}))).json()).error.code,-32602);
assert.equal((await worker.fetch(req('/api/decision',{method:'POST'}))).status,405);
assert.equal((await worker.fetch(req('/a2a',{method:'POST',body:'x'.repeat(9000)}))).status,413);
assert.equal((await worker.fetch(req('/a2a',{method:'POST',body:'{'}))).status,200);
const old=globalThis.fetch;globalThis.fetch=async()=>{throw Error('No RPC');};const fail=await worker.fetch(req('/api/decision'));assert.equal(fail.status,503);assert.equal((await fail.json()).decision,null);globalThis.fetch=old;
console.log('9 endpoint checks passed; no wallet methods or broadcasts');
if(process.argv.includes('--live')){const r=await worker.fetch(req('/api/decision'));const d=await r.json();assert.equal(r.status,200,JSON.stringify(d));assert.equal(d.chainId,97);console.log(JSON.stringify({live:true,decision:d.decision,weight:d.allocation.WBNBPercent,observedAt:d.observedAt}));}
