import json,time,urllib.request,concurrent.futures as cf,statistics as st
from collections import defaultdict
MV=10000.0   # min $ quote-volume in 24h on EACH side (kills dead markets)
BD=0.15      # each venue within 15% of the pair's median price (kills ticker-clash/outliers)
QUOTES=["USDT","USDC","FDUSD","TUSD","DAI","USD"]  # USD-stable quotes only (quote-vol ~ USD)
ALIAS={"XBT":"BTC","WETH":"ETH","WBTC":"BTC"}
FEES={"KuCoin":0.001,"OKX":0.001,"Gate.io":0.001,"MEXC":0.0005,"Crypto.com":0.00075}
E=[""]
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36"
def g(u):
 try:return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA,"Accept":"application/json"}),timeout=20))
 except Exception as e:E[0]=(E[0]+" | "+str(e)[:70])[-280:];return None
def norm(b):
 b=(b or "").upper();return ALIAS.get(b,b)
def fnum(x):
 try:return float(x)
 except Exception:return 0.0
def split_concat(sym):
 for q in QUOTES:
  if sym.endswith(q) and len(sym)>len(q):return sym[:-len(q)],q
 return None,None
def kucoin():
 d=g("https://api.kucoin.com/api/v1/market/allTickers");o=[]
 if d and isinstance(d.get("data"),dict):
  for t in d["data"].get("ticker") or []:
   s=t.get("symbol") or ""
   if "-" not in s:continue
   base,quote=s.split("-",1)
   if quote not in QUOTES:continue
   px=fnum(t.get("last"));vol=fnum(t.get("volValue"))
   if px>0:o.append(("KuCoin",norm(base),quote,px,vol))
 return o
def okx():
 d=g("https://www.okx.com/api/v5/market/tickers?instType=SPOT");o=[]
 if d and isinstance(d.get("data"),list):
  for t in d["data"]:
   s=t.get("instId") or ""
   if "-" not in s:continue
   base,quote=s.split("-",1)
   if quote not in QUOTES:continue
   px=fnum(t.get("last"));vol=fnum(t.get("volCcy24h"))
   if px>0:o.append(("OKX",norm(base),quote,px,vol))
 return o
def gate():
 d=g("https://api.gateio.ws/api/v4/spot/tickers");o=[]
 if isinstance(d,list):
  for t in d:
   s=t.get("currency_pair") or ""
   if "_" not in s:continue
   base,quote=s.split("_",1)
   if quote not in QUOTES:continue
   px=fnum(t.get("last"));vol=fnum(t.get("quote_volume"))
   if px>0:o.append(("Gate.io",norm(base),quote,px,vol))
 return o
def mexc():
 d=g("https://api.mexc.com/api/v3/ticker/24hr");o=[]
 if isinstance(d,list):
  for t in d:
   base,quote=split_concat(t.get("symbol") or "")
   if not quote:continue
   px=fnum(t.get("lastPrice"));vol=fnum(t.get("quoteVolume"))
   if px>0:o.append(("MEXC",norm(base),quote,px,vol))
 return o
def cryptocom():
 d=g("https://api.crypto.com/v2/public/get-ticker");o=[]
 res=(d or {}).get("result") or {}
 for t in res.get("data") or []:
  s=t.get("i") or ""
  if "_" not in s:continue
  base,quote=s.split("_",1)
  if quote not in QUOTES:continue
  px=fnum(t.get("a"));vol=fnum(t.get("v"))*px
  if px>0:o.append(("Crypto.com",norm(base),quote,px,vol))
 return o
SRCS=[kucoin,okx,gate,mexc,cryptocom]
def fetch():
 rows=[]
 with cf.ThreadPoolExecutor(len(SRCS)) as p:
  for r in p.map(lambda f:f(),SRCS):rows.extend(r)
 nv=len({r[0] for r in rows})
 return rows,nv,len(SRCS)
def gaps(rows):
 pr=defaultdict(list)
 for (ex,base,quote,px,vol) in rows:
  if vol<MV:continue
  pr[(base,quote)].append((ex,px,vol))
 res=[]
 for (base,quote),lst in pr.items():
  if len({x[0] for x in lst})<2:continue
  med=st.median([x[1] for x in lst])
  if med<=0:continue
  byv={}
  for ex,px,vol in lst:
   if abs(px/med-1)>BD:continue
   if ex not in byv or vol>byv[ex][2]:byv[ex]=(ex,px,vol)
  v=list(byv.values())
  if len(v)<2:continue
  v.sort(key=lambda x:x[1]);lo,hi=v[0],v[-1]
  gp=100*(hi[1]-lo[1])/lo[1]
  if gp<=0:continue
  bf=FEES.get(lo[0],0.001);sf=FEES.get(hi[0],0.001);net=(hi[1]*(1-sf)/(lo[1]*(1+bf))-1)*100
  res.append({"coin":base,"id":base,"quote":quote,"buy":lo[0],"buy_px":lo[1],"sell":hi[0],"sell_px":hi[1],"gap":round(gp,3),"fees":round((bf+sf)*100,3),"net":round(net,3),"venues":len(v),"dex":False,"vol":round(min(lo[2],hi[2]))})
 res.sort(key=lambda x:-x["gap"]);return res
def meta_of(res,nv,ns,secs):
 ist=time.strftime("%d %b %Y, %H:%M:%S IST",time.gmtime(time.time()+19800))
 return {"generated":ist,"opps":len(res),"venues_live":nv,"venues_total":ns,"venues_in_gaps":len({r["buy"] for r in res}|{r["sell"] for r in res}),"coins":len({r["id"] for r in res}),"seconds":secs,"refresh_sec":300,"min_vol":int(MV),"max_age":0,"err":E[0]}
