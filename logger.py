from os import path
from csv import writer
from datetime import datetime
from yfinance import Ticker
from config import Config 

class TradeLogger:
    def __init__(self, config: Config):
        self.trade_file = config.trade_file
        self.equity_file = config.equity_file
        
    def log_trade(self, symbol: str, amount: float, side: str):
        try:
            file_exists = path.exists(self.trade_file)
            with open(self.trade_file, mode='a', newline='',) as file:
                write = writer(file)
                if not file_exists:
                    write.writerow(['Date','Symbol','Price','Amount','Side'])

                price = Ticker(symbol).info.get('regularMarketPrice')
                if price is None:
                    price = 'N/A'
                
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                write.writerow([date, symbol, price, amount, side])
        except Exception as e:
            print(f'Error logging trade: {e}')

    def log_equity(self, account_value: float, rebalance_triggered: bool):
        try:
            file_exists = path.exists(self.equity_file)
            with open(self.equity_file, mode='a', newline='',) as file:
                write = writer(file)
                if not file_exists:
                    write.writerow(['Date',"Account Value", 'Rebalance'])
                
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                write.writerow([date, round(account_value, 2), str(rebalance_triggered).upper()])

        except Exception as e:
            print(f'Error logging account info: {e}')