import pandas as pd

from backtester.engine import Backtester
from strategies.moving_average import MovingAverageStrategy
from utils.exporter import save_results


def main():
    # =========================
    # USER INPUT
    # =========================
    file_path = "data/qqq_march_2026_5m.csv"                         #input("Enter data file (e.g., data/aapl.csv): ")
    initial_cash = 1000

    # =========================
    # LOAD DATA
    # =========================
    df = pd.read_csv(file_path)

    # Ensure correct format
    if "Close" not in df.columns:
        raise ValueError("CSV must contain a 'Close' column")

    if "Datetime" not in df.columns:
        raise ValueError("CSV must contain a 'Datetime' column")

    prices = df["Close"].tolist()
    timestamps = df["Datetime"].tolist()

    # =========================
    # INIT STRATEGY + BACKTESTER
    # =========================
    strategy = MovingAverageStrategy()

    backtester = Backtester(
        data=prices,
        timestamps=timestamps,
        strategy=strategy,
        initial_cash=initial_cash
    )

    # =========================
    # RUN BACKTEST
    # =========================
    final_value = backtester.run()

    # =========================
    # METRICS
    # =========================
    metrics = backtester.calculate_metrics(initial_cash)

    # =========================
    # PRINT RESULTS
    # =========================
    print("\n===== BACKTEST RESULTS =====")
    print(f"Final Portfolio Value: ${metrics['final_value']:.2f}")
    print(f"Final Cash: ${backtester.cash:.2f}")
    print(f"Final Position: {backtester.position} shares")
    print(f"Total Profit: ${metrics['total_profit']:.2f}")

    print("\n===== PERFORMANCE METRICS =====")
    print(f"Total Trades: {metrics['total_trades']}")
    print(f"Win Rate: {metrics['win_rate']:.2f}%")
    print(f"Average Profit per Trade: ${metrics['avg_profit']:.2f}")

    print("\n===== TRADE LOG =====")
    for trade in backtester.get_trade_log():
        print(trade)

    # =========================
    # SAVE RESULTS
    # =========================
    save_results(
        backtester.get_trade_log(),
        metrics,
        "results/backtest_results.csv"
    )

    print("\nResults saved to results/backtest_results.csv")


if __name__ == "__main__":
    main()