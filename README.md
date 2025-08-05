# EqualWeightRebalancer
This program maintains equal weights across a set of stocks and cash, rebalancing only when a stock deviates 10% from its target. Designed for use with Alpaca’s trading platform.

# Rebalancer 🤖

An automated portfolio rebalancing system that maintains target allocations using Alpaca Trading API. Automatically rebalances your portfolio when positions deviate more than 10% from target allocations.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Alpaca](https://img.shields.io/badge/Alpaca-Trading%20API-green)
![Automated](https://img.shields.io/badge/Automated-Rebalancing-orange)

## 🚀 Features

### 📊 **Automated Portfolio Rebalancing**
- **Threshold-based rebalancing** (10% deviation trigger)
- **Equal-weight portfolio** management
- **Cash buffer** protection
- **Market hours** detection and handling

### 🤖 **Scheduled Execution**
- **Daily/weekly scheduling** with configurable timing
- **Market open/close** detection
- **Error handling** and notifications
- **Trade logging** and performance tracking

### 📈 **Trading Integration**
- **Alpaca Trading API** integration
- **Real-time market data**
- **Automated order execution**
- **Position management**

### 📧 **Notifications & Logging**
- **Email notifications** for trades and errors
- **Detailed trade logging** to CSV files
- **Performance tracking** and reporting
- **Deviation reports** before rebalancing

## 🛠️ Tech Stack

- **Python 3.8+**
- **Alpaca Trading API** - Trading execution
- **APScheduler** - Task scheduling
- **SMTP** - Email notifications
- **CSV logging** - Trade and performance tracking

## 📦 Installation

### Prerequisites
- Python 3.8+
- Alpaca Trading account
- Gmail account (for notifications)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Rebalancer.git
   cd Rebalancer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```

4. **Configure your `.env` file**
   ```env
   # Alpaca Trading API
   ALPACA_API_KEY=your_alpaca_api_key
   ALPACA_SECRET_KEY=your_alpaca_secret_key
   BASE_URL=https://paper-api.alpaca.markets
   
   # Email Configuration
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_APP_PASSWORD=your_gmail_app_password
   EMAIL_RECEIVER=your_email@gmail.com
   
   # Portfolio Configuration
   STOCKS=PLTR,TOL,AMZN,NEM,CAT,UNH,DAL,LMT,KO
   
   # Scheduling
   DAY_OF_WEEK=1
   HOUR=9
   MINUTE=30
   TIMEZONE=America/New_York
   
   # File Paths
   TRADE_CSV=trades.csv
   EQUITY_CSV=equity.csv
   ```

5. **Run the rebalancer**
   ```bash
   python main.py
   ```

## 🎯 Usage

### Manual Execution
```bash
python main.py
```

### Scheduled Execution
The system automatically schedules rebalancing based on your configuration:
- **Day of week**: 1-7 (Monday-Sunday)
- **Time**: Hour and minute in your timezone
- **Market hours**: Only executes when market is open

### Configuration Options

#### Portfolio Stocks
Edit the `STOCKS` environment variable:
```env
STOCKS=AAPL,MSFT,GOOGL,TSLA,NVDA
```

#### Rebalancing Threshold
Modify the threshold in `strategy.py`:
```python
self.threshold = 0.10  # 10% deviation trigger
```

#### Cash Buffer
Adjust the cash buffer ratio:
```python
cash_buffer_ratio = 1 / (len(self.config.stocks) + 1)
```

## 📁 Project Structure

```
Rebalancer/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── alpaca_client.py     # Alpaca Trading API client
├── strategy.py          # Portfolio rebalancing logic
├── scheduler.py         # Task scheduling
├── notifier.py          # Email notifications
├── logger.py            # Trade and performance logging
├── performance.py       # Performance analysis
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── trades.csv          # Trade log file
├── equity.csv          # Performance tracking
└── README.md           # This file
```

## 🔧 Configuration Details

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ALPACA_API_KEY` | Your Alpaca API key | `PK...` |
| `ALPACA_SECRET_KEY` | Your Alpaca secret key | `...` |
| `BASE_URL` | Alpaca API base URL | `https://paper-api.alpaca.markets` |
| `EMAIL_SENDER` | Gmail address for sending | `your@gmail.com` |
| `EMAIL_APP_PASSWORD` | Gmail app password | `...` |
| `EMAIL_RECEIVER` | Email for notifications | `your@gmail.com` |
| `STOCKS` | Comma-separated stock symbols | `AAPL,MSFT,GOOGL` |
| `DAY_OF_WEEK` | Day to run (1=Monday) | `1` |
| `HOUR` | Hour to run (24-hour) | `9` |
| `MINUTE` | Minute to run | `30` |
| `TIMEZONE` | Your timezone | `America/New_York` |

### Trading Logic

1. **Market Check**: Only trades when market is open
2. **Position Cleanup**: Closes non-strategy positions
3. **Cash Buffer**: Reserves cash for emergencies
4. **Equal Allocation**: Divides remaining equity equally
5. **Threshold Check**: Only trades if deviation > 10%
6. **Order Execution**: Places market orders
7. **Logging**: Records all trades and performance

## 📊 Performance Tracking

The system automatically tracks:
- **Trade history** in `trades.csv`
- **Portfolio performance** in `equity.csv`
- **Email notifications** for all actions
- **Error logging** and reporting

## 🔒 Security

### API Keys
- Store API keys in `.env` file (not in code)
- Use paper trading for testing
- Never commit `.env` to version control

### Email Security
- Use Gmail App Passwords (not regular passwords)
- Enable 2-factor authentication
- Use dedicated email for notifications

## 🚨 Important Notes

### Paper Trading
- **Always test with paper trading first**
- Use Alpaca's paper trading environment
- Verify all functionality before live trading

### Risk Management
- **Cash buffer** protects against emergencies
- **Threshold-based** trading reduces unnecessary trades
- **Market hours** detection prevents after-hours trading
- **Error handling** prevents failed trades

### Monitoring
- **Check email notifications** regularly
- **Monitor trade logs** for accuracy
- **Review performance** data periodically
- **Test thoroughly** before live trading

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This software is for educational and personal use only. Trading involves risk, and you can lose money. Always test thoroughly with paper trading before using real money. The authors are not responsible for any financial losses.**

## 📞 Support

If you encounter any issues:
1. **Check the issues** page for existing solutions
2. **Create a new issue** with detailed information
3. **Review the logs** for error details

---

**Automated portfolio rebalancing made simple** 🤖 
