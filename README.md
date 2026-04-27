# Trading Strategy Backtester

A Python-based backtesting engine for testing trading strategies on historical market data.

## 🚀 Features

- Intraday (5-minute) data support
- Timestamp-based trade execution
- Moving average strategy with momentum & pullback logic
- Stop-loss and take-profit risk management
- Forced end-of-day exits (true day trading simulation)
- Trade logging and performance metrics

## 📊 Example Metrics

- Win Rate
- Total Profit
- Average Profit per Trade
- Trade Log with timestamps

## 🧠 Strategy Logic

- Trend confirmation using moving averages
- Pullback-based entries (buy dips in uptrends)
- Momentum filtering to avoid weak setups
- Risk management via stop-loss & take-profit

## 📁 Project Structure
trading-backtester/
│── backtester/
│ └── engine.py
│── strategies/
│ └── moving_average.py
│── utils/
│ └── exporter.py
│── data/
│── results/
│── main.py


## ⚡ How to Run

```bash
python main.py


---
