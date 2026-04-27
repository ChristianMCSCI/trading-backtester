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

        # Cooldown
        if index - self.last_trade_index < 15:
            return 0

        prices = data[:index+1]

        short_ma = sum(prices[-self.short_window:]) / self.short_window
        long_ma = sum(prices[-self.long_window:]) / self.long_window
        trend_ma = sum(prices[-self.trend_window:]) / self.trend_window

        price = prices[-1]

        # 🔥 NEW: momentum (price change over last 5 bars)
        momentum = (price - prices[-5]) / prices[-5]

        # 🔥 NEW: pullback (price below short MA)
        pullback = (short_ma - price) / short_ma

        # =========================
        # BUY (HIGH QUALITY ONLY)
        # =========================
        if short_ma > long_ma and price > trend_ma:

            # Strong trend
            if (short_ma - long_ma) / long_ma > 0.001:

                # Pullback entry (not chasing)
                if -0.002 < pullback < 0.03:

                    # Momentum turning back up
                    if momentum > -0.001:

                        self.last_trade_index = index
                        return 1

        # =========================
        # SELL
        # =========================
        elif short_ma < long_ma and price < trend_ma:
            return -1

        return 0