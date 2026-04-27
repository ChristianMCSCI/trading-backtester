from utils.data_fetcher import fetch_data

def main():
    fetch_data(
        ticker="QQQ",
        start="2026-03-01",
        end="2026-03-31",
        interval="5m",
        filename="data/qqq_march_2026_5m.csv"
    )

if __name__ == "__main__":
    main()