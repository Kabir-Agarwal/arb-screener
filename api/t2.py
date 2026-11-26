P=r"""th{position:sticky;top:0;background:var(--p2);color:var(--dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.5px;cursor:pointer}
th.n,td.n{text-align:right;font-family:var(--m)}tbody tr:hover{background:#151c25}.q{color:var(--dim);font-size:11px}.g{color:var(--acc);font-weight:700}
.tag{font-size:10px;padding:1px 5px;border-radius:4px;border:1px solid var(--ln);color:var(--warn);margin-left:6px}
.foot{color:var(--dim);font-size:11.5px;margin-top:18px;line-height:1.6}
.rk{color:var(--dim);font-family:var(--m);text-align:right;width:34px}tr.trh td{background:#0d131a;cursor:pointer;font-size:12px;padding:9px 10px}tr.trh:hover td{background:#111923}.tg{color:var(--dim);margin-right:4px;font-size:10px}.rng{color:var(--dim);font-size:11px;margin-left:8px}.tc{color:var(--dim);font-size:11px;font-family:var(--m);float:right}
@media(max-width:720px){.st{grid-template-columns:repeat(2,1fr)}.hs{display:none}}
</style></head><body><div class=wrap>
<header><div class=logo>A</div><div><h1>Arb Screener</h1><div class=sub><span class=dot></span><span id=live>live</span> &middot; same-coin gaps across 5 exchanges, auto-updating</div></div></header>
<div class=ban><b>What this is:</b> a live monitor of where the same coin quotes at different prices across venues. <b>Gross %</b> = raw gap; <b>Net %</b> = after each venue's taker fee (per row). Net still excludes withdrawal/network fees, transfer time and tax, which often erase small gaps. <b>Not a profit signal, not financial advice.</b> Live from 5 exchanges (KuCoin, OKX, Gate.io, MEXC, Crypto.com); USD-stable pairs, &gt;$10k/24h each side, price-sanity filtered.</div>
<div class=st id=st></div>
<div class=bar><input type=text id=q placeholder="filter coin / venue..."><label>min gap % <input type=number id=mg value=0 step=0.5 style=width:70px></label><span class=ct id=ct></span></div>
<table><thead><tr><th>#</th><th data-k=coin>Coin</th><th data-k=buy>Buy venue (low)</th><th class=n data-k=buy_px>Buy px</th><th data-k=sell>Sell venue (high)</th><th class=n data-k=sell_px>Sell px</th><th class=n data-k=gap>Gross %</th><th class="n hs" data-k=fees>Fees %</th><th class=n data-k=net>Net %</th><th class="n hs" data-k=venues>Venues</th><th class="n hs" data-k=vol>Min 24h vol</th></tr></thead><tbody id=rows></tbody></table>
<div class=foot id=foot></div></div>
<script>
var D=__DATA__,M=__META__;
function nf(n){if(n==null)return"-";var a=Math.abs(n);if(a>=1)return n.toLocaleString(undefined,{maximumFractionDigits:2});if(a>=.01)return n.toPrecision(4);return n.toPrecision(3)}
"""
