from utils.data_loader import load_data
from strategies.moving_average import MovingAverageStrategy
from backtester.engine import Backtester
from utils.exporter import save_results
import os


def main():
    
    # ===== CONFIG =====
    data_file = input("Enter data file (e.g., data/aapl.csv): ")
   
    if not os.path.exists(data_file):
        print(f"Data file {data_file} not found. Please run fetch_data.py first.")
        return
   
    initial_cash = 1000

    # ===== LOAD DATA =====
    data = load_data(data_file)

    # ===== SETUP STRATEGY =====
    strategy = MovingAverageStrategy(
        short_window=5,
        long_window=20
    )

    # ===== RUN BACKTEST =====
    backtester = Backtester(data, strategy, initial_cash)
    final_value = backtester.run()

    # ===== CALCULATE METRICS =====
    metrics = backtester.calculate_metrics(initial_cash)

    # ===== PRINT CLEAN RESULTS =====
    print("\n===== BACKTEST RESULTS =====")
    print(f"Final Portfolio Value: ${final_value:.2f}")
    print(f"Final Cash: ${backtester.cash:.2f}")
    print(f"Final Position: {backtester.position} shares")
    print(f"Total Profit: ${metrics['total_profit']:.2f}")

    print("\n===== PERFORMANCE METRICS =====")
    print(f"Total Trades: {metrics['total_trades']}")
    print(f"Win Rate: {metrics['win_rate']:.2f}%")
    print(f"Average Profit per Trade: ${metrics['avg_profit']:.2f}")

    # ===== PRINT TRADE LOG =====
    print("\n===== TRADE LOG =====")
    for trade in backtester.trades:
        print(
            f"[Day {trade['index']}] "
            f"{trade['type']} @ ${trade['price']} | "
            f"Cash: ${trade['cash']:.2f}, "
            f"Position: {trade['position']}"
        )

    # ===== SAVE RESULTS TO CSV =====
    save_results(
        trades=backtester.trades,
        metrics=metrics,
        filename="results/backtest_results.csv"
    )

    print("\nResults saved to results/backtest_results.csv")


# ===== ENTRY POINT =====
if __name__ == "__main__":
    main()