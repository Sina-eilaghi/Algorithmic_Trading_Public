from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class DataProvider(ABC):
    @abstractmethod
    def get_ohlcv(self, symbol: str, timeframe: str, lookback: int) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_latest_price(self, symbol: str) -> float:
        raise NotImplementedError
