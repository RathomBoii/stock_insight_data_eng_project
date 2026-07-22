import yfinance as yf
import os
import pandas as pd
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

def ingest_ticker_ohlc(ticker: str, lookback_period: str) -> pd.DataFrame:
    logger.info(f"[FETCH] {ticker} fetching from yfinance...")
    desired_ticker = yf.Ticker(ticker)
    return desired_ticker.history(period=lookback_period)


def write_parquet_ile(raw_file_path: str, data_frame: pd.DataFrame) -> None:
    """
    Write the DataFrame to a Parquet file at the specified path.
    """
    engine = "pyarrow"
    data_frame["ingestion_timestamp"] = datetime.now(timezone.utc).isoformat()
    os.makedirs(os.path.dirname(raw_file_path), exist_ok=True)
    data_frame.to_parquet(raw_file_path, engine=engine)



def main():
    """
    1.check if data by ingest date exists in raw layer
    2.if not exists, fetch data from yfinance and write to raw layer
    3.if exist, early return .
    """
    DATA_CONTEXT = DataContext.OHLC
    FILE_EXTENTION = FileExtention.PARQUET
    LOOKBACK_PERIOD = "10y"

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
            ticker_ohlc_data_frame = ingest_ticker_ohlc(symbol, LOOKBACK_PERIOD)
            ticker_ohlc_data_frame["industry"] = industry
            ticker_ohlc_data_frame["country"] = country
            ticker_ohlc_data_frame["name"] = name
            write_parquet_ile(constructed_file_path, ticker_ohlc_data_frame)
            logger.info(f"[OK] {symbol} ({country}/{industry}) written to {constructed_file_path}")
        except Exception as e:
            logger.error(f"[FAIL] {symbol} ({country}/{industry}): {e}", exc_info=True)

if __name__ == "__main__":
    main()

                