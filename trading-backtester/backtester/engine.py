class Backtester:
    def __init__(self, data, timestamps, strategy, initial_cash=1000):
        self.data = data
        self.timestamps = timestamps
        self.strategy = strategy
        self.cash = initial_cash
        self.position = 0
        self.trades = []

        # Risk management
        self.buy_price = None
        self.stop_loss_pct = 0.995 
        self.take_profit_pct = 1.01  

    def run(self):
        for i in range(len(self.data)):
            price = self.data[i]
            timestamp_full = str(self.timestamps[i])
            timestamp = timestamp_full[:16]

            # =========================
            # TIME HANDLING (UTC → EST)
            # =========================
            hour = int(timestamp_full[11:13])
            minute = int(timestamp_full[14:16])
            hour_est = hour - 4  # adjust if DST changes matter later

            # =========================
            # FORCE END-OF-DAY SELL (3:55 PM EST)
            # =========================
            if hour_est == 15 and minute >= 55 and self.position > 0:
                self.cash += self.position * price
                self.trades.append(
                    f"[{timestamp}] END-OF-DAY SELL @ ${price:.2f} | Cash: ${self.cash:.2f}"
                )
                self.position = 0
                self.buy_price = None
                continue

            # =========================
            # RISK MANAGEMENT
            # =========================
            if self.position > 0 and self.buy_price is not None:

                # Stop-loss
                if price <= self.buy_price * self.stop_loss_pct:
                    self.cash += self.position * price
                    self.trades.append(
                        f"[{timestamp}] STOP-LOSS SELL @ ${price:.2f} | Cash: ${self.cash:.2f}"
                    )
                    self.position = 0
                    self.buy_price = None
                    continue

                # Take-profit
                if price >= self.buy_price * self.take_profit_pct:
                    self.cash += self.position * price
                    self.trades.append(
                        f"[{timestamp}] TAKE-PROFIT SELL @ ${price:.2f} | Cash: ${self.cash:.2f}"
                    )
                    self.position = 0
                    self.buy_price = None
                    continue

            # =========================
            # STRATEGY SIGNAL
            # =========================
            signal = self.strategy.generate_signal(self.data, i)

            # BUY
            if signal == 1 and self.cash >= price:
                self.position += 1
                self.cash -= price
                self.buy_price = price
                self.trades.append(
                    f"[{timestamp}] BUY @ ${price:.2f} | Cash: ${self.cash:.2f}, Position: {self.position}"
                )

            # SELL
            elif signal == -1 and self.position > 0:
                self.cash += self.position * price
                self.trades.append(
                    f"[{timestamp}] SELL @ ${price:.2f} | Cash: ${self.cash:.2f}"
                )
                self.position = 0
                self.buy_price = None

        final_value = self.cash + self.position * self.data[-1]
        return final_value

    def get_trade_log(self):
        return self.trades

    def calculate_metrics(self, initial_cash):
        final_value = self.cash + self.position * self.data[-1]
        total_profit = final_value - initial_cash

        total_trades = len([t for t in self.trades if "SELL" in t])

        wins = 0
        profits = []

        for i in range(len(self.trades)):
            if "BUY" in self.trades[i] and i + 1 < len(self.trades):
                buy_price = float(self.trades[i].split("@ $")[1].split()[0])

                for j in range(i + 1, len(self.trades)):
                    if "SELL" in self.trades[j]:
                        sell_price = float(self.trades[j].split("@ $")[1].split()[0])
                        profit = sell_price - buy_price
                        profits.append(profit)
                        if profit > 0:
                            wins += 1
                        break

        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        avg_profit = (sum(profits) / len(profits)) if profits else 0

        return {
            "final_value": final_value,
            "total_profit": total_profit,
            "total_trades": total_trades,
            "win_rate": win_rate,
            "avg_profit": avg_profit
        }
