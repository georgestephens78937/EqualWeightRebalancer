from dotenv import load_dotenv
from os import getenv


class Config:
    env_path = env_path = "z:/Coding/Projects/Rebalancer/.env" # change if not on pc
    
    def __init__(self):
        load_dotenv(dotenv_path=self.env_path)
        self.api_key = getenv('ALPACA_API_KEY')
        self.secret_key = getenv('ALPACA_SECRET_KEY')
        self.base_url = getenv('BASE_URL')
        self.email_sender = getenv('EMAIL_SENDER')
        self.email_password = getenv('EMAIL_APP_PASSWORD')
        self.email_receiver = getenv('EMAIL_RECEIVER')
        self.stocks = getenv('STOCKS', 'PLTR,TOL,AMZN,NEM,CAT,UNH,DAL,LMT,KO').split(',')
        self.day_of_week = getenv('DAY_OF_WEEK')
        self.hour = getenv('HOUR')
        self.minute = getenv('MINUTE')
        self.timezone = getenv('TIMEZONE')
        self.trade_file = getenv('TRADE_CSV')
        self.equity_file = getenv('EQUITY_CSV')


    def validate(self):
        missing = [k for k, v in vars(self).items() if v in [None, '']]
        if missing:
            raise ValueError(f"Missing config variables: {missing}")