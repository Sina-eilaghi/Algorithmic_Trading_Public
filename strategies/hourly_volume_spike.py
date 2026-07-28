from __future__ import annotations

from typing import Optional

import pandas as pd

from .base import BaseStrategy, Signal


class HourlyVolumeSpikeStrategy(BaseStrategy):
    name = "hourly_volume_spike"
    timeframe = "1h"

    def __init__(self, volume_multiplier: float = 10.0, lookback_hours: int = 24, exclude_current_candle: bool = True):
        self.volume_multiplier = volume_multiplier
        self.lookback_hours = lookback_hours
        self.exclude_current_candle = exclude_current_candle

    def evaluate(self, df: pd.DataFrame) -> Optional[Signal]:
        if df.empty or len(df) < self.lookback_hours + 2:
            return None

        volume = pd.to_numeric(df["volume"], errors="coerce")
        if self.exclude_current_candle:
            window = volume.iloc[-self.lookback_hours - 2 : -1]
        else:
            window = volume.iloc[-self.lookback_hours - 1 : -1]
        current_volume = float(volume.iloc[-1])
        threshold = float(window.mean()) * self.volume_multiplier

        if current_volume > threshold:
            return Signal(
                asset="",
                strategy_name=self.name,
                timestamp=str(df.index[-1]),
                trigger_value=current_volume,
                threshold=threshold,
                volume=current_volume,
                price=float(df["close"].iloc[-1]),
                direction="spike",
            )
        return None
