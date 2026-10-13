const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),E=require('../dist/engine.js');
async function trial({chain='0x61',account=E.C.wallet,error=4001,double=false,lock=true,switchMode=null}={}){
 const ids=['connect','walletState','send','prepare','refresh','cash','asset','native','weight','actual','bar','sync','review','decisionBadge','decisionTitle','decisionText','details','expiry','status','txLink','recover'];
 const nodes=Object.fromEntries(ids.map(id=>[id,{disabled:false,hidden:true,textContent:'',style:{},replaceChildren(){},append(){}}])),store=new Map();let sends=0,switches=0,adds=0;
 const s={now:Math.floor(Date.now()/1000),cash:9n*10n**18n,asset:0n,native:10n**17n,weight:0};
 const p={kind:'APPROVE',snapshot:s,buy:true,approvalAmount:E.C.cap,amount:E.C.cap,cost:10n**13n,created:s.now,expires:s.now+300,tx:{from:E.C.wallet,to:E.C.cash,data:'0x095ea7b3'+E.aw(E.C.router)+E.word(E.C.cap),value:'0x0'}};
 const provider={request:async({method,params})=>{if(method==='wallet_switchEthereumChain'){switches++;assert.equal(params[0].chainId,'0x61');if(switchMode==='reject')throw Object.assign(Error('Rejected'),{code:4001});if(switchMode==='missing'&&adds===0)throw Object.assign(Error('Unknown chain'),{code:4902});if(switchMode==='ok'||switchMode==='missing'){chain='0x61';return null;}throw Error('Unsupported');}if(method==='wallet_addEthereumChain'){adds++;assert.equal(params[0].chainId,'0x61');assert.equal(params[0].rpcUrls[0],'https://bsc-testnet-dataseed.bnbchain.org');return null;}if(method==='eth_chainId')return chain;if(['eth_requestAccounts','eth_accounts'].includes(method))return [account];if(method==='eth_sendTransaction'){sends++;throw Object.assign(new Error('wallet result'),{code:error});}throw Error(method);}};
 const context={window:{TreasuryEngine:{...E,prepare:async()=>p,validateForSend:async()=>p,snapshot:async()=>s},ethereum:provider,addEventListener(){}},document:{getElementById:id=>nodes[id],createElement:()=>({textContent:''})},localStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)},navigator:{locks:{request:async(_,__,f)=>f(lock?{}:null)}},confirm:()=>false,setTimeout,Date,console};
 vm.createContext(context);vm.runInContext(fs.readFileSync('dist/app.js','utf8'),context);
 await nodes.prepare.onclick();if(double)await Promise.all([nodes.send.onclick(),nodes.send.onclick()]);else await nodes.send.onclick();return {sends,nodes,store,switches,adds};
}
(async()=>{
 assert.equal((await trial({chain:'0x38'})).sends,0,'wrong wallet network never opens transaction');
 assert.equal((await trial({account:E.C.asset})).sends,0,'wrong account never opens transaction');
 const rejected=await trial({double:true});assert.equal(rejected.sends,1,'double-click opens only one wallet request');assert.equal(rejected.store.size,0,'explicit wallet rejection clears pending marker');
 const unknown=await trial({error:-32000});assert.equal(unknown.sends,1);assert.equal(unknown.store.size,1,'ambiguous wallet failure retains pending marker');assert.equal(unknown.nodes.send.disabled,true);
 assert.equal((await trial({lock:false})).sends,0,'another active tab prevents wallet request');
 const switched=await trial({chain:'0x38',switchMode:'ok'});assert.equal(switched.switches,1);assert.equal(switched.sends,1);
 const cancelled=await trial({chain:'0x38',switchMode:'reject'});assert.equal(cancelled.sends,0);assert.equal(cancelled.store.size,0);
 const added=await trial({chain:'0x38',switchMode:'missing'});assert.equal(added.adds,1);assert.equal(added.switches,2);assert.equal(added.sends,1);
 console.log('8 UI flow checks passed with fake wallet; no real signature or broadcast.');
})().catch(e=>{console.error(e);process.exitCode=1;});
