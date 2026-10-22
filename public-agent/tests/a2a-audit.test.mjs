import assert from 'node:assert/strict';
import worker from '../worker/index.js';

const logs=[];
const originalInfo=console.info;
console.info=(message)=>logs.push(JSON.parse(message));
const send=async(text)=>worker.fetch(new Request('https://fual-treasury-agent.phamphuanloc.chatgpt.site/a2a',{method:'POST',body:JSON.stringify({jsonrpc:'2.0',id:'do-not-log-this-input',method:'message/send',params:{message:{role:'user',messageId:'test',parts:[{kind:'text',text}]}}})}));
try {
 const good=await send('evidence');
 assert.equal((await good.json()).result.role,'agent');
 assert.equal(logs.at(-1).rpcSuccess,true);
 assert.equal(logs.at(-1).readOnly,true);
 const bad=await send('do not publish private input');
 assert.equal(bad.status,200);
 assert.equal((await bad.json()).error.code,-32602);
 assert.equal(logs.at(-1).rpcSuccess,false);
 assert.equal(logs.at(-1).errorCode,-32602);
 assert.equal(JSON.stringify(logs).includes('do not publish private input'),false);
 assert.equal(JSON.stringify(logs).includes('do-not-log-this-input'),false);
} finally { console.info=originalInfo; }
console.log('A2A audit distinguishes JSON-RPC error from HTTP success and omits caller input');
