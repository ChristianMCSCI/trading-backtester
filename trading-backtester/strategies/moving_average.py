from yfinance import data
from strategies.base_strategy import Strategy
import pandas as pd

class MovingAverageStrategy:
    def __init__(self, short_window=5, long_window=20, trend_window=50):
        self.short_window = short_window
        self.long_window = long_window
        self.trend_window = trend_window
        self.last_trade_index = -100  # cooldown

    def generate_signal(self, data, index):
        if index < self.trend_window:
            return 0

        # Cooldown (prevents overtrading)
        if index - self.last_trade_index < 20:
            return 0

        prices = data[:index+1]

        short_ma = sum(prices[-self.short_window:]) / self.short_window
        long_ma = sum(prices[-self.long_window:]) / self.long_window
        trend_ma = sum(prices[-self.trend_window:]) / self.trend_window

        price = prices[-1]

        # 🕒 TIME FILTER (intraday only)
        # NOTE: only works if you pass timestamps later (optional for now)
        # timestamp = pd.to_datetime(data.index[index])
        # hour = timestamp.hour
        # if hour < 14 or hour > 19:
        #     return 0

        # 🔥 STRONG TREND FILTER
        if short_ma > long_ma and price > trend_ma:
            if (short_ma - long_ma) / long_ma > 0.002:
                self.last_trade_index = index
                return 1

        elif short_ma < long_ma and price < trend_ma:
            return -1

        return 0