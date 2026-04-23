from strategies.base_strategy import Strategy

class MovingAverageStrategy(Strategy):
    def __init__(self, short_window=5, long_window=20):
        # Number of days for short-term average
        self.short_window = short_window
        
        # Number of days for long-term average
        self.long_window = long_window

    def generate_signal(self, data, index):
        # Not enough data yet to calculate moving averages
        if index < self.long_window:
            return 0  # HOLD

        # Calculate short-term moving average
        short_avg = sum(data[index - self.short_window:index]) / self.short_window

        # Calculate long-term moving average
        long_avg = sum(data[index - self.long_window:index]) / self.long_window

        # If short-term trend is above long-term → BUY
        if short_avg > long_avg:
            return 1

        # If short-term trend is below long-term → SELL
        elif short_avg < long_avg:
            return -1

        # Otherwise do nothing
        return 0