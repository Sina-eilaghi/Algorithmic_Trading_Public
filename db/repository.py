from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .schema import DB_PATH, init_db


class SignalRepository:
    def __init__(self, conn: sqlite3.Connection | None = None):
        self.conn = conn or init_db()

    def log_signal(self, signal: Any) -> None:
        self.conn.execute(
            """
            INSERT INTO signals (asset, strategy_name, timestamp, trigger_value, threshold, price, volume, direction, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                signal.asset,
                signal.strategy_name,
                signal.timestamp,
                signal.trigger_value,
                signal.threshold,
                signal.price,
                signal.volume,
                signal.direction,
                json.dumps(signal.metadata or {}),
            ),
        )
        self.conn.commit()

    def get_signal_stats(self, strategy_name: str, asset: str | None = None) -> dict[str, Any]:
        query = "SELECT COUNT(*) FROM signals WHERE strategy_name = ?"
        params: list[Any] = [strategy_name]
        if asset:
            query += " AND asset = ?"
            params.append(asset)
        count = self.conn.execute(query, params).fetchone()[0]
        return {"count": count}
