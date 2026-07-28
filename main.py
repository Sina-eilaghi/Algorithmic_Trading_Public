from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler

from bot.telegram_bot import TelegramNotifier
from scheduler.engine import AlertEngine


if __name__ == "__main__":
    notifier = TelegramNotifier()
    engine = AlertEngine(notifier=notifier)
    engine.run()

    scheduler = BlockingScheduler()
    scheduler.add_job(engine.run, "interval", hours=1)
    scheduler.add_job(engine.run, "cron", hour=0, minute=1)
    scheduler.start()
