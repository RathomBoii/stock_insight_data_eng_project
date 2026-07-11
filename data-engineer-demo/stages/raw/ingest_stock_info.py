from types import MappingProxyType

import yfinance as yf
import json
import os

# Variables
from TICKERS import TICKERS

# Utils
from utils.construct_raw_data_file_path import construct_raw_data_file_path, DataContext
from utils.check_existing_raw_data import check_existing_raw_data

"""
1.loop through TICKERS
2.fetch history for each ticker
3.store fetch data in raw layer partitioned by ingestion date
"""

def ingest_ticker_info(ticker: str) -> dict:
    print(f"Fetching {ticker} info from yfinance...")
    desired_ticker = yf.Ticker(ticker)
    return desired_ticker.info

def write_json_file(data: dict, file_path: str) -> None:
    # 'with open' acts as a context manager; it automatically closes the file 
    # safely when the block finishes, preventing memory leaks or data corruption.
    # "w" is write mode, "r" for read mode
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    """
    1.check if data by ingest date exists in raw layer
    2.if not exists, fetch data from yfinance and write to raw layer
    3.if exist, early return .
    """
    DESIRED_TICKERS : MappingProxyType[str, dict[str, dict[str, str]]] = TICKERS
    DATA_CONTEXT = DataContext.INFO

    for industry, countries in DESIRED_TICKERS.items():
        """
        We got in
            {
        ! we're here ->
                "Cloud Provider": {
                    "US": {"MSFT": "MSFT", "AMZN": "AMZN ...
                },
                "SaaS": {
                    "US": {"CRM": "CRM", "NOW": "NOW" ...
                }
            }
        """
        for country, tickers in countries.items():
            """
        !   we're here -> 
                "US": {"MSFT": "MSFT", "AMZN": "AMZN", "GOOGL": "GOOGL"},
            """
            for ticker_name, ticker_symbol in tickers.items():
                """
                1.contruct file path
                2.fecth data from yfinance
                3.write data to raw layer
                """
                print(f"ticker_name: {ticker_name}, ticker_symbol: {ticker_symbol}")

                constructed_file_path = construct_raw_data_file_path(ticker_name, DATA_CONTEXT)

                is_raw_data_already_exist = check_existing_raw_data(constructed_file_path)

                if is_raw_data_already_exist:
                    print(f"The info data for {ticker_symbol} of {country} are already existed in RAW layer, skipping the fetching process...")
                    continue
                else:
                    print(f"Fetching info data for {ticker_symbol} of {country} from yfinance")
                    ticker_history_info = ingest_ticker_info(ticker_symbol)
                    write_json_file(ticker_history_info, constructed_file_path)

# ✅ Case 1: main() was called at top-level → runs unintentionally on import.
# ✅ Case 2: this file is imported by ingest_all.py → guard is required.
if __name__ == "__main__":
    main()

                