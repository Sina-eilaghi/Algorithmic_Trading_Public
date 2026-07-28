from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class Signal:
    asset: str
    strategy_name: str
    timestamp: str
    trigger_value: float
    threshold: float
    price: Optional[float] = None
    volume: Optional[float] = None
    direction: Optional[str] = None
    metadata: Optional[dict] = None


class BaseStrategy(ABC):
    name: str = ""
    timeframe: str = ""

    @abstractmethod
    def evaluate(self, df: pd.DataFrame) -> Optional[Signal]:
        """Return a Signal if the condition is met, otherwise None."""
        raise NotImplementedError
