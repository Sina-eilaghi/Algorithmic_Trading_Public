import pandas as pd

from strategies.daily_bollinger_breakout import DailyBollingerBreakoutStrategy
from strategies.hourly_volume_spike import HourlyVolumeSpikeStrategy
from strategies.base import Signal


def test_daily_bollinger_breakout_fires_when_price_hits_upper_band():
    df = pd.DataFrame(
        {
            "close": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 40],
        }
    )
    strategy = DailyBollingerBreakoutStrategy(std_multiplier=2.2, lookback_days=20)

    signal = strategy.evaluate(df)

    assert signal is not None
    assert signal.strategy_name == "daily_bollinger_breakout"
    assert signal.direction in {"upper", "lower"}
    assert signal.trigger_value >= signal.threshold


def test_hourly_volume_spike_fires_for_large_recent_volume():
    base_volumes = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    window = list(base_volumes) + [5000]
    df = pd.DataFrame({"volume": window, "close": [1] * len(window)})

    strategy = HourlyVolumeSpikeStrategy(volume_multiplier=10, lookback_hours=24, exclude_current_candle=True)
    signal = strategy.evaluate(df)

    assert signal is not None
    assert signal.strategy_name == "hourly_volume_spike"
    assert signal.trigger_value > signal.threshold
