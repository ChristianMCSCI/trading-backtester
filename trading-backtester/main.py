from utils.data_loader import load_data
from strategies.moving_average import MovingAverageStrategy
from backtester.engine import Backtester

def main():
    # Load price data from CSV
    data = load_data('data/sample_data.csv')

    # Create strategy instance
    strategy = MovingAverageStrategy()

    # Create backtester with data + strategy
    backtester = Backtester(data, strategy)

    # Run simulation
    result = backtester.run()

    # Print final result
    print(f"Final Portfolio Value: {result}")

# Entry point of program
if __name__ == "__main__":
    main()