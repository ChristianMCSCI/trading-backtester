import yfinance as yf

def fetch_data(ticker="AAPL", start="2022-01-01", end="2023-01-01", filename="data/aapl.csv"):
    data = yf.download(ticker, start=start, end=end)

    if data.empty:
        print("ERROR: No data downloaded.")
        return

    # 🔥 Flatten multi-index columns (THIS FIXES YOUR ISSUE)
    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    data.to_csv(filename)

    print(f"Data saved to {filename} ({len(data)} rows)")