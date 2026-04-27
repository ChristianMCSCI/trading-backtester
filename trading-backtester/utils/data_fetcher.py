import yfinance as yf
import pandas as pd

def fetch_data(ticker, start, end, filename, interval="1d"):
    data = yf.download(
        ticker,
        start=start,
        end=end,
        interval=interval,
        progress=False
    )

    if data.empty:
        print("❌ No data fetched.")
        return

    # Flatten columns if needed (yfinance sometimes returns multi-index)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data.to_csv(filename)
    print(f"✅ Data saved to {filename} ({len(data)} rows)")