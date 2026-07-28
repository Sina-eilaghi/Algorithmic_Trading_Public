import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "alerts.db"


def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset TEXT NOT NULL,
            strategy_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            trigger_value REAL NOT NULL,
            threshold REAL NOT NULL,
            price REAL,
            volume REAL,
            direction TEXT,
            metadata TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cache (
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            lookback INTEGER NOT NULL,
            payload TEXT NOT NULL,
            PRIMARY KEY (symbol, timeframe, lookback)
        )
        """
    )
    conn.commit()
    return conn
