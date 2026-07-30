from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler

from bot.telegram_bot import TelegramNotifier
from scheduler.engine import AlertEngine


if __name__ == "__main__":
    notifier = TelegramNotifier() # This is the object used to send alerts.
    engine = AlertEngine(notifier=notifier) # This is the part that actually checks the market and decides whether a signal should be triggered.
    engine.run()

    scheduler = BlockingScheduler()
    scheduler.add_job(engine.run, "interval", hours=1)
    scheduler.add_job(engine.run, "cron", hour=0, minute=1)
    scheduler.start()
