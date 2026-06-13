import yfinance as yf
import numpy as np
import pandas as pd

TICKERS = ["NVDA", "GOOGL", "AMD", "META", "NFLX"]

def fetch_prices(days=500):
    raw = yf.download(TICKERS, period=f"{days}d", auto_adjust=True, progress=False)["Close"]
    return raw[TICKERS].dropna()

def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices / prices.shift(1)).dropna()
