P=r"""function mo(n){return"$"+Number(n).toLocaleString()}
function stats(){var np=D.filter(function(d){return d.net>0}).length;document.getElementById('st').innerHTML=[["Opportunities",M.opps.toLocaleString()],["Net-positive",np.toLocaleString()],["Venues",M.venues_live+" / "+M.venues_total],["Coins",M.coins.toLocaleString()],["Scan",M.seconds+"s"]].map(function(x){return '<div class=c><div class=k>'+x[0]+'</div><div class=v>'+x[1]+'</div></div>'}).join('')}
var sk="net",sd=-1;
var collapsed={strong:false,mod:false,thin:true,neg:true};
var TIERS=[{k:"strong",lab:"Strong",rng:"net &gt; 2%",col:"var(--acc)",f:function(d){return d.net>2}},{k:"mod",lab:"Moderate",rng:"net 0.5-2%",col:"#2bb3d4",f:function(d){return d.net>0.5&&d.net<=2}},{k:"thin",lab:"Thin",rng:"net 0-0.5%",col:"var(--warn)",f:function(d){return d.net>0&&d.net<=0.5}},{k:"neg",lab:"Negative after fees",rng:"net &le; 0%",col:"var(--red)",f:function(d){return d.net<=0}}];
function cell(d,i){return '<tr><td class=rk>'+(i+1)+'</td><td>'+d.coin+' <span class=q>'+d.quote+'</span></td><td>'+d.buy+'</td><td class=n>'+nf(d.buy_px)+'</td><td>'+d.sell+'</td><td class=n>'+nf(d.sell_px)+'</td><td class="n g">'+d.gap.toFixed(2)+'%</td><td class="n hs" style="color:var(--dim)">'+d.fees.toFixed(2)+'%</td><td class=n style="color:'+(d.net>0?'var(--acc)':'var(--red)')+';font-weight:700">'+d.net.toFixed(2)+'%</td><td class="n hs">'+d.venues+'</td><td class="n hs">'+mo(d.vol)+'</td></tr>'}
function rnd(){
 var q=document.getElementById('q').value.toLowerCase(),mg=parseFloat(document.getElementById('mg').value)||0;
 var r=D.filter(function(d){if(d.gap<mg)return false;if(q){if((d.coin+" "+d.id+" "+d.quote+" "+d.buy+" "+d.sell).toLowerCase().indexOf(q)<0)return false}return true});
 r.sort(function(a,b){var x=a[sk],y=b[sk];if(typeof x==="string"){x=x.toLowerCase();y=(y||"").toLowerCase()}return x<y?sd:x>y?-sd:0});
 var html="";
 TIERS.forEach(function(T){var g=r.filter(T.f);if(!g.length)return;var open=!collapsed[T.k];html+='<tr class=trh data-k="'+T.k+'"><td colspan=11><span class=tg>'+(open?'&#9662;':'&#9656;')+'</span><b style="color:'+T.col+'">'+T.lab+'</b><span class=rng>'+T.rng+'</span><span class=tc>'+g.length+' pairs</span></td></tr>';if(open)html+=g.slice(0,400).map(cell).join('')});
 document.getElementById('rows').innerHTML=html||'<tr><td colspan=11 style="color:var(--dim);padding:20px">No rows match.</td></tr>';
 document.getElementById('ct').textContent=r.length.toLocaleString()+" pairs";
}
Array.prototype.forEach.call(document.querySelectorAll('thead th'),function(th){th.onclick=function(){var k=th.getAttribute('data-k');if(!k)return;if(sk===k)sd=-sd;else{sk=k;sd=(k==="coin"||k==="buy"||k==="sell")?1:-1}rnd()}});
document.getElementById('rows').addEventListener('click',function(e){var t=e.target;while(t&&t.nodeName!=="TR")t=t.parentNode;if(t&&(""+t.className).indexOf("trh")>=0){var k=t.getAttribute('data-k');collapsed[k]=!collapsed[k];rnd()}});
document.getElementById('q').oninput=rnd;document.getElementById('mg').oninput=rnd;
document.getElementById('foot').innerHTML="Net = gross minus both legs' taker fee. Assumed taker fees: KuCoin 0.10%, OKX 0.10%, Gate.io 0.10%, MEXC 0.05%, Crypto.com 0.075% (varies by VIP tier). Net still excludes withdrawal/network fees, transfer time and tax. Coins matched by ticker + 15% price-sanity band. Scanned "+M.generated+". <b>Not financial advice.</b>";
stats();rnd();
var last=Date.now();
function poll(){fetch('?json=1&t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){if(j&&j.data){D=j.data;M=j.meta;last=Date.now();stats();rnd()}}).catch(function(){})}
setInterval(poll,5000);
setInterval(function(){var el=document.getElementById('live');if(el)el.textContent='updated '+Math.round((Date.now()-last)/1000)+'s ago'},1000);
</script></body></html>"""
