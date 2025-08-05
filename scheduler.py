from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from strategy import PortfolioStrategy
from pytz import timezone
from config import Config


class RebalanceScheduler:
    def __init__(self, strategy: PortfolioStrategy, config: Config):
        self.scheduler = BlockingScheduler()
        self.strategy = strategy
        self.config = config

    def schedule_daily(self):
        self.scheduler.add_job(
            func=self.strategy.rebalance,
            trigger=CronTrigger(
                day_of_week=self.config.day_of_week, 
                hour=self.config.hour,                    
                minute=self.config.minute,
                timezone=timezone(self.config.timezone)
                ),
            id='daily_rebalance'
        )

    def run(self):
        try:
            print("\n--- Alpaca Equal Weight Rebalance Bot with Scheduler ---")
            print('        Running every trading day at 10:00 AM CT')
            self.scheduler.start()
            
        except (KeyboardInterrupt, SystemExit):
            print('Scheduler stopped.')