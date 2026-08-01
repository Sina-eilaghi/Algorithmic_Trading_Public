from __future__ import annotations

import asyncio
import os
from typing import Any

from dotenv import load_dotenv
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config.loader import ConfigManager
from db.repository import SignalRepository

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()


class TelegramNotifier:
    def __init__(self, token: str | None = None, chat_id: str | None = None):
        self.token = token or TOKEN
        self.chat_id = chat_id or CHAT_ID

    def send_message(self, message: str) -> None:
        if not self.token or not self.chat_id:
            return
        asyncio.run(self._send_message(message))

    async def _send_message(self, message: str) -> None:
        async with Bot(token=self.token) as bot:
            await bot.send_message(chat_id=self.chat_id, text=message)


class AlertBot:
    def __init__(self, config_manager: ConfigManager | None = None, repository: SignalRepository | None = None):
        if not TOKEN:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is missing. Add it to the project .env file.")
        self.config_manager = config_manager or ConfigManager()
        self.repository = repository or SignalRepository()
        self.application = Application.builder().token(TOKEN).build()
        self._register_handlers()

    def _register_handlers(self) -> None:
        self.application.add_handler(CommandHandler("start", self._start))
        self.application.add_handler(CommandHandler("status", self._status))
        self.application.add_handler(CommandHandler("activate", self._activate))
        self.application.add_handler(CommandHandler("deactivate", self._deactivate))
        self.application.add_handler(CommandHandler("kpis", self._kpis))
        self.application.add_handler(CommandHandler("list_assets", self._list_assets))
        self.application.add_handler(CommandHandler("help", self._help))

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = ReplyKeyboardMarkup(
            [
                [KeyboardButton("/status"), KeyboardButton("/list_assets")],
                [KeyboardButton("/help")],
            ],
            resize_keyboard=True,
            is_persistent=True,
        )
        await update.message.reply_text(
            "Alert bot is active. Choose an option below:",
            reply_markup=keyboard,
        )

    async def _status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        lines = ["Strategies:"]
        for name in ["daily_bollinger_breakout", "hourly_volume_spike"]:
            state = "active" if self.config_manager.get_strategy_state(name) else "inactive"
            lines.append(f"- {name}: {state}")
        await update.message.reply_text("\n".join(lines))

    async def _activate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /activate <strategy> [asset]")
            return
        strategy_name = args[0]
        asset_name = args[1] if len(args) >= 2 else None
        self.config_manager.set_strategy_state(strategy_name, True, asset_name)
        await update.message.reply_text(f"Enabled strategy {strategy_name}")

    async def _deactivate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /deactivate <strategy> [asset]")
            return
        strategy_name = args[0]
        asset_name = args[1] if len(args) >= 2 else None
        self.config_manager.set_strategy_state(strategy_name, False, asset_name)
        await update.message.reply_text(f"Disabled strategy {strategy_name}")

    async def _kpis(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        args = context.args
        strategy_name = args[0] if args else "daily_bollinger_breakout"
        asset = args[1] if len(args) > 1 else None
        stats = self.repository.get_signal_stats(strategy_name, asset)
        await update.message.reply_text(f"{strategy_name}: {stats}")

    async def _list_assets(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assets = []
        for group, items in self.config_manager.data.get("assets", {}).items():
            assets.append(f"{group}: {', '.join(item['name'] for item in items)}")
        await update.message.reply_text("\n".join(assets))

    async def _help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        help_text = "\n".join([
            "/status - show strategies and assets",
            "/activate <strategy> [asset] - enable a strategy",
            "/deactivate <strategy> [asset] - disable a strategy",
            "/kpis <strategy> [asset] - show KPI summary",
            "/list_assets - show configured assets",
            "/help - show this help",
        ])
        await update.message.reply_text(help_text)

    def run(self) -> None:
        self.application.run_polling()
