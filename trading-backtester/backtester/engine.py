class Backtester:
    def __init__(self, data, strategy, initial_cash=1000):
        self.data = data
        self.strategy = strategy
        self.cash = initial_cash
        self.position = 0
        # Track completed trades (buy → sell pairs)
        self.completed_trades = []
        # Track last buy price
        self.last_buy_price = None
        # NEW: store all trades
        self.trades = []

    def run(self):
        for i in range(len(self.data)):
            signal = self.strategy.generate_signal(self.data, i)
            price = self.data[i]

            # BUY
            if signal == 1 and self.cash >= price and self.position == 0:
                self.position += 1
                self.cash -= price

                self.last_buy_price = price # remember buy price for profit calculation

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

                # Calculate profit for this trade
                if self.last_buy_price is not None:
                    profit = price - self.last_buy_price
                    
                    self.completed_trades.append({
                        "buy_price": self.last_buy_price,
                        "sell_price": price,
                        "profit": profit
                    })
                    
                    self.last_buy_price = None # reset after selling

                # LOG TRADE
                self.trades.append({
                    "type": "SELL",
                    "price": price,
                    "index": i,
                    "cash": self.cash,
                    "position": self.position
                })
        if self.position > 0:
            final_price = self.data[-1]
            self.cash += final_price
            self.position = 0
        final_value = self.cash + self.position * self.data[-1]
        return final_value

    def calculate_metrics(self, initial_cash):
        total_trades = len(self.completed_trades)

        if total_trades == 0:
            return {
                "total_profit": 0,
                "total_trades": 0,
                "win_rate": 0,
                "avg_profit": 0
        }

        total_profit = sum(t["profit"] for t in self.completed_trades)
        winning_trades = [t for t in self.completed_trades if t["profit"] > 0]
       
        win_rate = len(winning_trades) / total_trades * 100
        avg_profit = total_profit / total_trades

        return {
            "total_profit": total_profit,
            "total_trades": total_trades,
            "win_rate": win_rate,
            "avg_profit": avg_profit
        }