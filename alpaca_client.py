from alpaca_trade_api import REST
from config import Config
class AlpacaClient:
    def __init__(self, config: Config):
        self.api = REST(config.api_key, config.secret_key, config.base_url)

    def is_market_open(self):
        return self.api.get_clock().is_open
    
    def get_account_info(self):
        return self.api.get_account()
    
    def get_positions(self):
        return self.api.list_positions()
    
    def submit_order(self, symbol: str, notional: float, side: str):
        self.api.submit_order(
            symbol=symbol,
            notional=notional,
            side=side,
            type='market',
            time_in_force='day'
        )