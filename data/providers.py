from __future__ import annotations

from typing import Any

import pandas as pd
import yfinance as yf

from .base import DataProvider


class YahooFinanceProvider(DataProvider):
    def get_ohlcv(self, symbol: str, timeframe: str, lookback: int) -> pd.DataFrame:
        interval = "1d" if timeframe == "1d" else "1h"
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=f"{lookback + 30}d", interval=interval, auto_adjust=False)
        if df.empty:
            return pd.DataFrame(columns=["close", "volume"])
        df = df[["Close", "Volume"]].rename(columns={"Close": "close", "Volume": "volume"})
        return df.dropna()

    def get_latest_price(self, symbol: str) -> float:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d", interval="1d")
        if data.empty:
            raise ValueError(f"No market data for {symbol}")
        return float(data["Close"].iloc[-1])


class CryptoProvider(DataProvider):
    def get_ohlcv(self, symbol: str, timeframe: str, lookback: int) -> pd.DataFrame:
        raise NotImplementedError("ccxt integration can be added later")

    def get_latest_price(self, symbol: str) -> float:
        raise NotImplementedError("ccxt integration can be added later")
