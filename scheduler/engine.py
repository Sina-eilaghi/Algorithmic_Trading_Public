from __future__ import annotations

import logging
from typing import Any

from config.loader import ConfigManager
from data.providers import YahooFinanceProvider
from db.repository import SignalRepository
from strategies.daily_bollinger_breakout import DailyBollingerBreakoutStrategy
from strategies.hourly_volume_spike import HourlyVolumeSpikeStrategy

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class AlertEngine:
    # This class is responsible for running the alert engine, which checks the market for signals based on the configured strategies and assets. Also save signals to the database and sends notifications if a signal is triggered.
    def __init__(self, config_manager: ConfigManager | None = None, repository: SignalRepository | None = None, notifier: Any | None = None):
        self.config_manager = config_manager or ConfigManager()
        self.repository = repository or SignalRepository()
        self.notifier = notifier
        self.data_provider = YahooFinanceProvider()
        self.strategies = {
            "daily_bollinger_breakout": DailyBollingerBreakoutStrategy(**self._strategy_params("daily_bollinger_breakout")),
            "hourly_volume_spike": HourlyVolumeSpikeStrategy(**self._strategy_params("hourly_volume_spike")),
        }

    def _strategy_params(self, strategy_name: str) -> dict[str, Any]:
        strategy_config = self.config_manager.data.get("strategies", {}).get(strategy_name, {})
        return strategy_config.get("params", {})

    def run(self) -> None:
        for strategy_name, strategy in self.strategies.items():
            for asset_group_name, assets in self.config_manager.data.get("assets", {}).items():
                for asset in assets:
                    if not self.config_manager.get_strategy_state(strategy_name, asset.get("name")):
                        continue
                    ticker = self._resolve_ticker(asset, strategy_name)
                    if not ticker:
                        continue
                    try:
                        df = self.data_provider.get_ohlcv(ticker, strategy.timeframe, 100)
                        signal = strategy.evaluate(df)
                        if signal:
                            signal.asset = asset["name"]
                            signal.metadata = {"ticker": ticker, "group": asset_group_name}
                            self.repository.log_signal(signal)
                            logger.info("Signal fired: %s for %s", strategy_name, asset["name"])
                            self._notify(signal)
                    except Exception as exc:  # pragma: no cover
                        logger.exception("Failed to evaluate %s for %s: %s", strategy_name, asset["name"], exc)

    def _notify(self, signal: Any) -> None:
        if self.notifier is None:
            return
        message = (
            f"Alert: {signal.asset}\n"
            f"Strategy: {signal.strategy_name}\n"
            f"Direction: {signal.direction or 'n/a'}\n"
            f"Trigger: {signal.trigger_value:.2f}\n"
            f"Threshold: {signal.threshold:.2f}\n"
            f"Price: {signal.price if signal.price is not None else 'n/a'}"
        )
        self.notifier.send_message(message)

    def _resolve_ticker(self, asset: dict[str, Any], strategy_name: str) -> str | None:
        if strategy_name in asset.get("ticker_overrides", {}):
            return asset["ticker_overrides"][strategy_name]
        return asset.get("ticker")
