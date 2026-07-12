import yfinance as yf
import json
import os
import logging
from datetime import datetime, timezone

# Variables
from TICKERS import TICKERS

# Utils
from utils.construct_raw_data_file_path import construct_raw_data_file_path, DataContext, FileExtention
from utils.check_existing_raw_data import check_existing_raw_data

"""
1.loop through TICKERS
2.fetch history for each ticker
3.store fetch data in raw layer partitioned by ingestion date
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

#  __name__ refer to the current .py file, make the log easier to be investigated.
logger = logging.getLogger(__name__)

def ingest_ticker_info(ticker: str) -> dict:
    print(f"Fetching {ticker} info from yfinance...")
    desired_ticker = yf.Ticker(ticker)
    return desired_ticker.info

def write_json_file(data: dict, file_path: str) -> None:
    # 'with open' acts as a context manager; it automatically closes the file 
    # safely when the block finishes, preventing memory leaks or data corruption.
    # "w" is write mode, "r" for read mode
    data["ingestion_timestamp"] = datetime.now(timezone.utc).isoformat()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    """
    1.check if data by ingest date exists in raw layer
    2.if not exists, fetch data from yfinance and write to raw layer
    3.if exist, early return .
    """
    DATA_CONTEXT = DataContext.INFO
    FILE_EXTENTION = FileExtention.JSON

    for ticker in TICKERS:
        industry   = ticker["industry"]
        country    = ticker["country"]
        name       = ticker["name"]
        symbol     = ticker["symbol"]
        delisted   = ticker["delisted"]

        if delisted:
            logger.info(f"[SKIP] {symbol} ({name}) is delisted, skipping.")
            continue

        constructed_file_path = construct_raw_data_file_path(symbol, DATA_CONTEXT, FILE_EXTENTION)
        is_raw_data_already_exist = check_existing_raw_data(constructed_file_path)

        if is_raw_data_already_exist:
            logger.info(f"[SKIP] {symbol} ({country}/{industry}) already exists in RAW layer.")
            continue

        try:
            logger.info(f"[FETCH] {symbol} ({country}/{industry}) fetching from yfinance...")
            ticker_history_info = ingest_ticker_info(symbol)
            ticker_history_info["industry"] = industry
            ticker_history_info["country"] = country
            ticker_history_info["name"] = name
            write_json_file(ticker_history_info, constructed_file_path)
            logger.info(f"[OK] {symbol} ({country}/{industry}) written to {constructed_file_path}")
        except Exception as e:
            logger.error(f"[FAIL] {symbol} ({country}/{industry}): {e}", exc_info=True)

# ✅ Case 1: main() was called at top-level → runs unintentionally on import.
# ✅ Case 2: this file is imported by ingest_all.py → guard is required.
if __name__ == "__main__":
    main()

                