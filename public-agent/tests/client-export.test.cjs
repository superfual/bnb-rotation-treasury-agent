const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const E=require('../client-ui/engine.js');
function setup({clipboard=true,blockedDownload=false,badJournal=false}={}){
 const nodes=new Map(),get=id=>{if(!nodes.has(id))nodes.set(id,{hidden:true,value:'',textContent:'',style:{},children:[],append(x){this.children.push(x)},replaceChildren(){this.children=[]},focus(){this.focused=true},select(){this.selected=true}});return nodes.get(id)};
 const hash='0x'+'a'.repeat(64),journal={schema:'fual-owner-approved-execution-v1',entries:[{event:'BROADCAST',data:{hash}},{event:'CONFIRMED',data:{hash}},{event:'DECISION',data:{hash:'javascript:alert(1)'}}]};
 let writes=[],revoked=0,downloads=0,reads=0;const body={append(){}};
 const context={window:{TreasuryEngine:E,TreasuryEvidence:{readJournal:async()=>{reads++;if(badJournal)throw Error('journal invalid');return journal}},addEventListener(){}},document:{getElementById:get,body,createElement:()=>({append(x){this.child=x},click(){downloads++},remove(){}})},localStorage:{getItem:()=>null,setItem(){throw Error('export must not change storage')},removeItem(){throw Error('export must not change storage')}},navigator:{clipboard:clipboard?{writeText:async t=>writes.push(t)}:undefined},Blob:class {},URL:{createObjectURL(){if(blockedDownload)throw Error('blocked');return 'blob:test'},revokeObjectURL(){revoked++}},setTimeout:()=>{},Date,console};
 vm.createContext(context);vm.runInContext(fs.readFileSync('client-ui/app.js','utf8'),context);
 return {get,journal,hash,writes,stats:()=>({downloads,reads,revoked})};
}
(async()=>{
 const a=setup();await a.get('exportEvidence').onclick();assert.equal(a.get('evidencePanel').hidden,false);assert.deepEqual(JSON.parse(a.get('evidenceText').value),a.journal);assert.equal(a.stats().downloads,0,'opening export never attempts an unsupported download');assert.equal(a.get('evidenceTransactions').children.length,1,'deduplicate txs and exclude invalid links');assert.equal(a.get('evidenceTransactions').children[0].child.href,'https://testnet.bscscan.com/tx/'+a.hash);await a.get('copyEvidence').onclick();assert.equal(a.writes[0],a.get('evidenceText').value);
 const b=setup({clipboard:false,blockedDownload:true});await b.get('exportEvidence').onclick();await b.get('copyEvidence').onclick();assert.equal(b.get('evidenceText').selected,true);b.get('downloadEvidence').onclick();assert.match(b.get('evidenceStatus').textContent,/không hỗ trợ tải/);assert.deepEqual(JSON.parse(b.get('evidenceText').value),b.journal,'blocked download preserves full selectable journal');
 const c=setup();await c.get('exportEvidence').onclick();c.get('downloadEvidence').onclick();assert.equal(c.stats().downloads,1);assert.match(c.get('evidenceStatus').textContent,/không xác nhận/,'download request is not claimed as completed');
 const d=setup({badJournal:true});await d.get('exportEvidence').onclick();assert.equal(d.get('evidencePanel').hidden,true);assert.match(d.get('status').textContent,/journal invalid/);
 console.log('Mobile export: blocked download/clipboard keeps selectable JSON, safe deduplicated receipt links, no wallet/network/storage writes, no false download-success claim.');
})().catch(e=>{console.error(e);process.exitCode=1});
