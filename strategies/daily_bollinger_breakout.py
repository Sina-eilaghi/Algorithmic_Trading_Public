from __future__ import annotations

from typing import Optional

import pandas as pd

from .base import BaseStrategy, Signal


class DailyBollingerBreakoutStrategy(BaseStrategy):
    name = "daily_bollinger_breakout"
    timeframe = "1d"

    def __init__(self, std_multiplier: float = 2.2, lookback_days: int = 20):
        self.std_multiplier = std_multiplier
        self.lookback_days = lookback_days

    def evaluate(self, df: pd.DataFrame) -> Optional[Signal]:
        if df.empty or len(df) < self.lookback_days + 1:
            return None

        close = pd.to_numeric(df["close"], errors="coerce")
        sma = close.rolling(window=self.lookback_days).mean().iloc[-2]
        std = close.rolling(window=self.lookback_days).std().iloc[-2]
        upper = sma + self.std_multiplier * std
        lower = sma - self.std_multiplier * std
        latest_price = float(close.iloc[-1])

        if latest_price >= upper:
            return Signal(
                asset="",
                strategy_name=self.name,
                timestamp=str(df.index[-1]),
                trigger_value=latest_price,
                threshold=upper,
                price=latest_price,
                direction="upper",
            )
        if latest_price <= lower:
            return Signal(
                asset="",
                strategy_name=self.name,
                timestamp=str(df.index[-1]),
                trigger_value=latest_price,
                threshold=lower,
                price=latest_price,
                direction="lower",
            )
        return None
