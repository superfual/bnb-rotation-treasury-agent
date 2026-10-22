import assert from 'node:assert/strict';
import worker from '../worker/index.js';
const url='https://fual-treasury-agent.phamphuanloc.chatgpt.site';
let r=await worker.fetch(new Request(url+'/rebalance/'));
assert.equal(r.status,200);const html=await r.text();
assert.match(html,/Chưa kết nối/);assert.match(html,/chưa thu phí/);assert.doesNotMatch(html,/0xdcf6…FA709/);
assert.match(r.headers.get('Content-Security-Policy'),/bsc-testnet-dataseed.bnbchain.org/);
for(const file of ['engine.js','app.js','evidence.js','style.css']){
 r=await worker.fetch(new Request(url+'/rebalance/'+file));assert.equal(r.status,200,file);assert.equal(r.headers.get('Cache-Control'),'no-store');assert.ok((await r.text()).length>100);
}
assert.equal((await worker.fetch(new Request(url+'/rebalance/package.json'))).status,404);
assert.equal((await worker.fetch(new Request(url+'/rebalance/secret.env'))).status,404);
assert.equal((await worker.fetch(new Request(url+'/rebalance/',{method:'POST'}))).status,405);
assert.equal((await worker.fetch(new Request(url+'/rebalance/',{method:'HEAD'}))).status,200);
assert.equal((await worker.fetch(new Request(url+'/rebalance'))).status,308);
console.log('Public beta asset whitelist, content, CSP, methods and redirect checks passed');
