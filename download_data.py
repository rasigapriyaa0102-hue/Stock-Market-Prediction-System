import yfinance as yf
import os

stocks = [
"TCS.NS",
"RELIANCE.NS",
"INFY.NS",
"HDFCBANK.NS",
"ICICIBANK.NS",
"SBIN.NS",
"LT.NS",
"ITC.NS",
"KOTAKBANK.NS",
"HINDUNILVR.NS"
]

os.makedirs("data", exist_ok=True)

for stock in stocks:

    df = yf.download(stock,start="2019-01-01",end="2025-12-31")

    name = stock.replace(".NS","")

    df.to_csv(f"data/{name}.csv")

print("Dataset Downloaded")