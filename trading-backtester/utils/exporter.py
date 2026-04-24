import csv

def save_results(trades, metrics, filename="results.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write metrics at the top
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Profit", metrics["total_profit"]])
        writer.writerow(["Total Trades", metrics["total_trades"]])
        writer.writerow(["Win Rate (%)", f"{metrics['win_rate']:.2f}"])
        writer.writerow(["Average Profit", f"{metrics['avg_profit']:.2f}"])

        writer.writerow([])  # blank line

        # Write trade log header
        writer.writerow(["Day", "Type", "Price", "Cash", "Position"])

        # Write trades
        for trade in trades:
            writer.writerow([
                trade["index"],
                trade["type"],
                trade["price"],
                trade["cash"],
                trade["position"]
            ])