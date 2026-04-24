from utils.data_fetcher import fetch_data

def main():
    fetch_data(
        ticker="QQQ",
        start="2025-01-01",
        end="2026-01-01",
        filename="data/qqq_2025.csv"
    )

if __name__ == "__main__":
    main()