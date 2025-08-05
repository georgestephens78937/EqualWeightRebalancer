from config import Config
from alpaca_client import AlpacaClient
from logger import TradeLogger
from notifier import Notifier

class PortfolioStrategy:
    def __init__(self, config: Config, alpaca: AlpacaClient, logger: TradeLogger, notifier: Notifier):
        self.config = config
        self.alpaca = alpaca
        self.logger = logger
        self.notifier = notifier
        self.threshold = 0.10 # Rebalances at a 10% deviation 
        self.min_buying_power = 1

    def close_non_strategy_positions(self):
        positions = self.alpaca.get_positions()
        for pos in positions:
            if pos.symbol not in self.config.stocks:
                print(f'\nClosing non-strategy positions: {pos.symbol}')
                try:
                    notional_amount = round(abs(float(pos.market_value)), 2)
                    if notional_amount < 1:
                        print(f'Skipping {pos.symbol}: amount to small.')
                        continue

                    side = 'sell' if float(pos.qty) > 0 else 'buy'
                    self.alpaca.submit_order(pos.symbol, notional_amount, side )
                except Exception as e:
                    print(f'Error clearing')

    def generate_deviation_report(self, positions, target_alloc):
        deviations = []
        for symbol, current_value in positions.items():
            diff_pct = (current_value - target_alloc) / target_alloc
            deviations.append((symbol, diff_pct))

        deviations.sort(key=lambda x: abs(x[1]), reverse=True)

        report_lines = ["Deviations Before Rebalance:"]
        for symbol, diff in deviations:
            direction = '+' if diff > 0 else ''
            report_lines.append(f"{symbol}: {direction}{diff:.2%} from target.")

        return "\n".join(report_lines)

    def rebalance(self):
        try:
            if not self.alpaca.is_market_open():
                msg = 'Market is Closed. Skipping Rebalance'
                print(msg)
                self.notifier.send('\u26d4 Rebalance Skipped', msg)
                return
            
            self.close_non_strategy_positions()

            account = self.alpaca.get_account_info()
            buying_power = float(account.buying_power)
            equity = float(account.equity)

            positions = {pos.symbol: float(pos.market_value) for pos in self.alpaca.get_positions()}
            cash_buffer_ratio = 1 / (len(self.config.stocks) + 1)
            reserve_cash = equity * cash_buffer_ratio
            target_alloc = (equity - reserve_cash) / len(self.config.stocks)
            
            report = self.generate_deviation_report(positions, target_alloc)
            self.notifier.send("Before Rebalance Deviations Report", report)

            if buying_power <= self.min_buying_power:
                msg = f'Buying power is too low: ${buying_power:.2f}. Skipping Rebalance...'
                print(msg)
                self.notifier.send('Low Buying Power', msg)
                return
            
            print(f'\nReserving ${reserve_cash} as a cash buffer.\n')
            actions = []

            for symbol in self.config.stocks:
                current_value = positions.get(symbol, 0)
                diff = (current_value - target_alloc) / target_alloc

                if abs(diff) > self.threshold:
                    notional = round(abs(target_alloc - current_value), 2)
                    if notional < 1:
                        print(f'${notional:.2f} of {symbol} is to small to place. Skipping...')
                        continue
                
                    side = 'sell' if current_value > target_alloc else 'buy'
                    action = f'{"Selling" if side == "sell" else "Buying"} ${notional:.2f} of {symbol}'
                    print(action)
                    self.alpaca.submit_order(symbol, notional, side)
                    self.logger.log_trade(symbol, notional, side)
                    actions.append(action)

                else: print(f'{symbol} within threshold. No action.')
            
            if actions:
                self.notifier.send("\u2705 Rebalance Executed", "\n".join(actions))
            else:
                self.notifier.send("\u2705 Rebalance Checked", "No trades needed. All positions within threshold.")
                                
            self.logger.log_equity(float(account.equity), bool(actions))
        
        except Exception as e:
            print(f'Error Rebalancing Portfolio: {e}')
            self.notifier.error_send(str(e))