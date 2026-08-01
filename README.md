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
2. Copy the environment file and fill in the credentials from BotFather and your
   numeric Telegram chat ID:
   ```bash
   cp .env.example .env
   ```
   ```dotenv
   TELEGRAM_BOT_TOKEN=123456789:replace-with-your-bot-token
   TELEGRAM_CHAT_ID=123456789
   ```
3. Run the complete service (Telegram command bot plus scheduled market scans):
   ```bash
   python main.py
   ```

4. Open the bot in Telegram, press **Start**, then try:
   ```text
   /status
   /list_assets
   /help
   ```

Sending `/start` also displays a persistent keyboard containing **Status**,
**List assets**, and **Help** command buttons.

The first market scan starts immediately. Further scans run hourly. Stop the
service with `Ctrl+C`.

### Getting your chat ID

Send a message to the bot, then open the following URL in a browser, replacing
`<TOKEN>` with the token supplied by BotFather:

```text
https://api.telegram.org/bot<TOKEN>/getUpdates
```

Use the numeric value under `message.chat.id` as `TELEGRAM_CHAT_ID`. Treat the
bot token as a password and never commit the `.env` file.

## Notes

- The initial implementation uses Yahoo Finance for stocks and commodities and a stub for crypto data via ccxt.
- The bot supports basic status, activation, deactivation, KPI, asset listing, and help commands.
- Strategies are configuration-driven and can be toggled without code changes.
