from __future__ import annotations

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from bot.telegram_bot import AlertBot, TelegramNotifier
from scheduler.engine import AlertEngine


def main() -> None:
    notifier = TelegramNotifier()
    if not notifier.token or not notifier.chat_id:
        raise RuntimeError(
            "Telegram configuration is incomplete. Add TELEGRAM_BOT_TOKEN and "
            "TELEGRAM_CHAT_ID to the project .env file."
        )

    alert_bot = AlertBot()
    engine = AlertEngine(notifier=notifier)

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        engine.run,
        "interval",
        hours=1,
        next_run_time=datetime.now(),
        id="hourly_market_scan",
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()

    try:
        alert_bot.run()
    finally:
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    main()
