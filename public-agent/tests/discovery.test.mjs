import assert from 'node:assert/strict';
import worker from '../worker/index.js';
const origin='https://fual-treasury-agent.phamphuanloc.chatgpt.site';
const request=(path,method='GET',body)=>new Request(origin+path,{method,...(body?{body:JSON.stringify(body)}:{})});
const payload={jsonrpc:'2.0',id:'probe',method:'message/send',params:{message:{role:'user',messageId:'probe-message',parts:[{kind:'text',text:'evidence'}]}}};
const card=await(await worker.fetch(request('/.well-known/agent-card.json'))).json();
assert.deepEqual(card.supportedInterfaces,[{url:origin+'/a2a',protocolBinding:'JSONRPC',protocolVersion:'0.3.0'}]);
for(const path of ['/a2a','/a2a/','/a2a/a2a','/.well-known/agent-card.json','/.well-known/agent.json']){
 const r=await worker.fetch(request(path,'POST',payload));
 assert.equal(r.status,200,path);const d=await r.json();assert.equal(d.id,'probe');assert.equal(d.result.role,'agent');assert.equal(d.result.metadata.readOnly,true);
 const denied=await(await worker.fetch(request(path,'POST',{...payload,method:'trade'}))).json();assert.equal(denied.error.code,-32601,path);
 const invalid=await(await worker.fetch(request(path,'POST',{...payload,params:{message:{...payload.params.message,role:'agent'}}}))).json();assert.equal(invalid.error.code,-32602,path);
}
const robots=await worker.fetch(request('/robots.txt'));assert.equal(robots.status,200);assert.match(await robots.text(),/Allow: \//);
for(const path of ['/','/.well-known/agent-card.json','/health']){const r=await worker.fetch(request(path,'HEAD'));assert.equal(r.status,200);assert.equal(await r.text(),'');}
assert.equal((await worker.fetch(request('/unknown','HEAD'))).status,404);
assert.equal((await worker.fetch(request('/a2a','DELETE'))).status,405);
console.log('Discovery checks passed: observed probe paths, HEAD, robots, and unchanged RPC permissions');
