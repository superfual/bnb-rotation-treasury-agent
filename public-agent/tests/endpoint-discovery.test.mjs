import assert from 'node:assert/strict';
import worker from '../worker/index.js';
const base='https://fual-treasury-agent.phamphuanloc.chatgpt.site';
const old=globalThis.fetch;globalThis.fetch=async()=>{throw Error('Discovery must not call RPC');};
try {
 const r=await worker.fetch(new Request(base+'/a2a'));assert.equal(r.status,200);const d=await r.json();assert.equal(d.transportInfo.discoveryOnly,true);assert.equal(d.transportInfo.invokeMethod,'POST');assert.equal(d.transportInfo.checksTestnet,false);assert.equal(d.url,base+'/a2a');assert.equal(d.result,undefined);
 const head=await worker.fetch(new Request(base+'/a2a',{method:'HEAD'}));assert.equal(head.status,200);assert.equal(await head.text(),'');
 const alias=await worker.fetch(new Request(base+'/.well-known/agent-registration.json'));assert.equal(alias.status,308);assert.equal(alias.headers.get('location'),base+'/registration.json');
 const post=await worker.fetch(new Request(base+'/a2a',{method:'POST',body:JSON.stringify({jsonrpc:'2.0',id:1,method:'message/send',params:{message:{role:'user',messageId:'check',parts:[{kind:'text',text:'status'}]}}})}));const fail=await post.json();assert.equal(fail.error.code,-32000);assert.equal(fail.result,undefined);
 console.log('Discovery compatibility passed; no fake live decision when RPC fails.');
} finally {globalThis.fetch=old;}
