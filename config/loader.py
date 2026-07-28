from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "default_config.yaml"
OVERRIDES_PATH = ROOT / "db" / "strategy_overrides.json"


class ConfigManager:
    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or CONFIG_PATH
        self.overrides_path = OVERRIDES_PATH
        self.data = self._load_yaml()
        self._ensure_override_file()

    def _load_yaml(self) -> dict[str, Any]:
        with self.config_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def _ensure_override_file(self) -> None:
        self.overrides_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.overrides_path.exists():
            self.overrides_path.write_text("{}", encoding="utf-8")

    def get_strategy_state(self, strategy_name: str, asset_name: str | None = None) -> bool:
        overrides = self._read_overrides()
        override_key = self._override_key(strategy_name, asset_name)
        if override_key in overrides:
            return overrides[override_key].get("enabled", True)
        if asset_name:
            return bool(self.data.get("strategies", {}).get(strategy_name, {}).get("enabled", True))
        return bool(self.data.get("strategies", {}).get(strategy_name, {}).get("enabled", True))

    def set_strategy_state(self, strategy_name: str, enabled: bool, asset_name: str | None = None) -> None:
        overrides = self._read_overrides()
        overrides[self._override_key(strategy_name, asset_name)] = {"enabled": enabled}
        self._write_overrides(overrides)

    def get_asset_ticker(self, asset_name: str, strategy_name: str) -> str | None:
        for asset_group in self.data.get("assets", {}).values():
            for asset in asset_group:
                if asset.get("name") == asset_name:
                    overrides = asset.get("ticker_overrides", {})
                    return overrides.get(strategy_name) or asset.get("ticker")
        return None

    def _override_key(self, strategy_name: str, asset_name: str | None = None) -> str:
        return f"{strategy_name}:{asset_name}" if asset_name else strategy_name

    def _read_overrides(self) -> dict[str, Any]:
        with self.overrides_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_overrides(self, payload: dict[str, Any]) -> None:
        with self.overrides_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
