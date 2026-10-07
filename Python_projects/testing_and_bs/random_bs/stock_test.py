import yfinance as yf
import pandas as pd
from io import StringIO
import requests
import pickle

with open("data.pkl", "rb") as g:
    df = pickle.load(g)

#response = requests.get(
#    "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
#)
#from io import StringIO
#tickers = pd.read_csv(StringIO(response.text))["Symbol"].tolist()
#tickers = [t.replace(".", "-") for t in tickers]

#df = yf.download((tickers), start="2015-01-01", end="2025-01-01", interval="1d", auto_adjust=True)

opens = df["Open"]
closes = df["Close"]  # already adjusted when auto_adjust=True

prev_close = closes.shift(1)
on = (opens - prev_close) / prev_close
cumulative_returns = (1 + on).prod() - 1

print(cumulative_returns.mean())

with open("data.pkl", "wb") as g:
    pickle.dump(df, g)