import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from http.server import BaseHTTPRequestHandler
import json,time
from scan_mod import fetch,gaps,meta_of
from t1 import P as P1
from t2 import P as P2
from t3 import P as P3
T=P1+P2+P3
def scan():
 t0=time.time();rows,act,tot=fetch();res=gaps(rows)
 return res,meta_of(res,act,tot,round(time.time()-t0,1))
class handler(BaseHTTPRequestHandler):
 def do_GET(self):
  ct="text/html; charset=utf-8"
  try:
   res,meta=scan()
   if "json" in (self.path or ""):
    body=json.dumps({"data":res,"meta":meta},separators=(",",":"));ct="application/json"
   else:
    body=T.replace("__DATA__",json.dumps(res,separators=(",",":"))).replace("__META__",json.dumps(meta))
  except Exception:
   body="<!doctype html><meta charset=utf-8><body style='padding:40px;font:16px sans-serif;background:#0a0e14;color:#e6edf3'><h1>Arb Screener</h1><p>Scan temporarily unavailable. Refresh in a moment.</p></body>"
  b=body.encode("utf-8")
  self.send_response(200)
  self.send_header("Content-Type",ct)
  self.send_header("Cache-Control","public, s-maxage=3, stale-while-revalidate=20")
  self.send_header("Content-Length",str(len(b)))
  self.end_headers()
  self.wfile.write(b)
