from pandas import read_csv
import matplotlib.pyplot as plt
import seaborn as sns

equity_df = read_csv('Rebalancer/equity.csv', parse_dates=['Date'])
trades_df = read_csv('Rebalancer/trades.csv', parse_dates=['Date'])

risk_free_rate = 0.04 # t-bill

def sharpe():
    try:
        # ( expected returns - risk free ) / volitility of returns
        returns = equity_df['Account Value'].pct_change()
        expected_returns = returns.sum()
        volitility = returns.std()

        sharpe = (expected_returns - risk_free_rate) / volitility

        return round(sharpe, 2)
    except Exception as e:
        print(f'Error calculating Sharpe Ratio: {e}')

def sortino():
    try:
        # ( expected returns - risk free ) / volitility of negative returns

        returns = equity_df['Account Value'].pct_change()
        negative_returns = returns[returns < 0]
        volitility = negative_returns.std()
        expected_returns = returns.sum()

        sortino =( expected_returns - risk_free_rate) / volitility
        return round(sortino, 2)

    except Exception as e:
        print(f'Error calulating Sorinto Ratio: {e}')

def total_return():
    try:
        start = equity_df['Account Value'].iloc[0]
        end = equity_df['Account Value'].iloc[-1]
        return round((end-start)/start * 100, 2)
    except Exception as e: print(e)

def max_drawdown():
    try:
        values = equity_df['Account Value']
        running_max = values.cummax()
        drawdowns = (values - running_max) / running_max
        max_drawdown = drawdowns.min()
        return round(max_drawdown, 4) * 100
    except Exception as e:
        print(f'Error calculating max drawdown: {e}')
 
def graph(sharpe: float, sortino: float, total_return: float, max_drawdown: float):
    try:
        sns.set_style("whitegrid")
        plt.figure(figsize=(14, 7))
        ax = sns.lineplot(
            data=equity_df,
            x='Date',
            y='Account Value',
            hue='Rebalance',
            palette='coolwarm',
            linewidth=2.5,
            marker='o'
        )
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Portfolio Value', fontsize=14)
        plt.title(
            f'Rebalancer Performance\n'
            f'Sharpe: {sharpe} | Sortino: {sortino} | Total Return: {total_return}% | Max Drawdown: {max_drawdown}%',
            fontsize=16,
            fontweight='bold'
        )
        plt.legend(title='Rebalance Triggered', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
        sns.despine()
        # Show only every 5th date label
        xticks = ax.get_xticks()
        ax.set_xticks(xticks[::5])
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f'Error graphing: {e}') 

try:
    graph(sharpe(), sortino(), total_return(), max_drawdown())
except Exception as e: print(f'Error Running: {e}')