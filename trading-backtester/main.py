from utils.data_loader import load_data
from strategies.moving_average import MovingAverageStrategy
from backtester.engine import Backtester

def main():
    data = load_data('data/sample_data.csv')

    strategy = MovingAverageStrategy()
    backtester = Backtester(data, strategy)

    result = backtester.run()

    # ===== CLEAN OUTPUT =====
    print("\n===== BACKTEST RESULTS =====")
    print(f"Final Portfolio Value: ${result:.2f}")
    print(f"Final Cash: ${backtester.cash:.2f}")
    print(f"Final Position: {backtester.position} shares")

    print("\n===== TRADE LOG =====")

    for trade in backtester.trades:
        print(
            f"[Day {trade['index']}] "
            f"{trade['type']} @ ${trade['price']} | "
            f"Cash: ${trade['cash']:.2f}, "
            f"Position: {trade['position']}"
        )