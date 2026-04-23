class Backtester:
    def __init__(self, data, strategy, initial_cash = float(input("Enter initial cash amount: "))):
        # List of prices (e.g., closing prices)
        self.data = data

        # Strategy object (must follow Strategy interface)
        self.strategy = strategy

        # Starting money
        self.cash = initial_cash

        # Number of shares currently held
        self.position = 0

    def run(self):
        # Loop through each time step (day)
        for i in range(len(self.data)):
            # Get BUY / SELL / HOLD signal from strategy
            signal = self.strategy.generate_signal(self.data, i)

            # Current price
            price = self.data[i]

            # BUY condition
            if signal == 1 and self.cash >= price:
                self.position += 1       # Buy 1 share
                self.cash -= price       # Deduct cost

            # SELL condition
            elif signal == -1 and self.position > 0:
                self.position -= 1       # Sell 1 share
                self.cash += price       # Add cash

        # Final portfolio value:
        # remaining cash + value of held shares
        final_value = self.cash + self.position * self.data[-1]

        return final_value