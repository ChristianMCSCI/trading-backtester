class Backtester:
    def __init__(self, data, strategy, initial_cash=1000):
        self.data = data
        self.strategy = strategy
        self.cash = initial_cash
        self.position = 0

        # NEW: store all trades
        self.trades = []

    def run(self):
        for i in range(len(self.data)):
            signal = self.strategy.generate_signal(self.data, i)
            price = self.data[i]

            # BUY
            if signal == 1 and self.cash >= price:
                self.position += 1
                self.cash -= price

                # LOG TRADE
                self.trades.append({
                    "type": "BUY",
                    "price": price,
                    "index": i,
                    "cash": self.cash,
                    "position": self.position
                })

            # SELL
            elif signal == -1 and self.position > 0:
                self.position -= 1
                self.cash += price

                # LOG TRADE
                self.trades.append({
                    "type": "SELL",
                    "price": price,
                    "index": i,
                    "cash": self.cash,
                    "position": self.position
                })

        final_value = self.cash + self.position * self.data[-1]
        return final_value