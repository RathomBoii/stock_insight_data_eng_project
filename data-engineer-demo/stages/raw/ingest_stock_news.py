import yfinance as yf
import logging
from typing import Any

# Variables
from TICKERS import TICKERS

# Utils
from utils.construct_raw_data_file_path import construct_raw_data_file_path, DataContext, FileExtention
from utils.check_existing_raw_data import check_existing_raw_data
from utils.write_json_file import write_json_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

#  __name__ refer to the current .py file, make the log easier to be investigated.
logger = logging.getLogger(__name__)

def ingest_ticker_new(ticker: str) -> list[dict[str, Any]]:
    try:
        logger.info(f"[OK] Ingest ticker: {ticker}'s news from yfinance.")
        news = yf.Ticker(ticker).news
        return news
    except Exception as e:
        logger.error(f"[FAIL] Ingest ticker: {ticker}'s news from yfinance: {e}", exc_info=True)
        return []

def main():
    """
    1.check if data by ingest date exists in raw layer
    2.if not exists, fetch data from yfinance and write to raw layer
    3.if exist, early return .
    """
    DATA_CONTEXT = DataContext.NEWS
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
            ticker_news = ingest_ticker_new(symbol)
            news_payload = {
                "ticker": symbol,
                "name": name,
                "industry": industry,
                "country": country,
                "news": ticker_news,
            }
            write_json_file(news_payload, constructed_file_path)
            logger.info(f"[OK] {symbol} ({country}/{industry}) written to {constructed_file_path}")
        except Exception as e:
            logger.error(f"[FAIL] {symbol} ({country}/{industry}): {e}", exc_info=True)

# Case 1: main() was called at top-level → runs unintentionally on import.
# Case 2: this file is imported by ingest_all.py → guard is required.
if __name__ == "__main__":
    main()

                