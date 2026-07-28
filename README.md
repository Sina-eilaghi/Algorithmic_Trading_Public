# Algorithmic_Trading_Public

This project provides a modular Python trading bot and alert system for monitoring crypto, stocks, and commodities using pluggable strategies and Telegram notifications.

## Structure

- strategies/: strategy interfaces and implementations
- data/: data providers and abstractions
- bot/: Telegram bot handlers
- config/: YAML config and runtime overrides
- db/: SQLite schema and repository helpers
- scheduler/: orchestration and scanning loop

## Quick start

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy the environment file and fill in your Telegram credentials:
   ```bash
   cp .env.example .env
   ```
3. Run the engine locally:
   ```bash
   python main.py
   ```

## Notes

- The initial implementation uses Yahoo Finance for stocks and commodities and a stub for crypto data via ccxt.
- The bot supports basic status, activation, deactivation, KPI, asset listing, and help commands.
- Strategies are configuration-driven and can be toggled without code changes.
