from config import Config
from alpaca_client import AlpacaClient
from logger import TradeLogger
from notifier import Notifier
from strategy import PortfolioStrategy
from scheduler import RebalanceScheduler


def main():
    try:
        config = Config()
        config.validate()
        alpaca = AlpacaClient(config)

        logger = TradeLogger(config)
        notifier = Notifier(config)
        strategy = PortfolioStrategy(config, alpaca, logger, notifier)
        scheduler = RebalanceScheduler(strategy, config) # Config here is for thr timing of scheduler

        scheduler.schedule_daily()
        scheduler.run()
        
    except Exception as e: 
        print(f'Error running main: {e}')
        notifier.error_send(str(e))

if __name__ == '__main__':
    main()