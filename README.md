# Arb Screener

Live crypto cross-exchange price-gap screener. Pulls spot tickers from 5 exchanges
(KuCoin, OKX, Gate.io, MEXC, Crypto.com), compares the same coin across venues on
USD-stable pairs, filters for liquidity + price sanity, and shows gross and
net-after-fees gaps. Auto-refreshes every ~5s.

Vercel Python serverless function (`api/index.py`), zero dependencies, public data only.
Not financial advice; gaps are gross/ net-of-trading-fees only and exclude withdrawal,
transfer time and tax.
