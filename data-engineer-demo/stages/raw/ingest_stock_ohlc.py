from types import MappingProxyType

import yfinance as yf
import os
import pandas as pd

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

def ingest_ticker_ohlc(ticker: str, lookback_period: str) -> pd.DataFrame:
    print(f"Fetching {ticker} from yfinance...")
    desired_ticker = yf.Ticker(ticker)
    return desired_ticker.history(period=lookback_period)


def write_parquet_ile(raw_file_path: str, data_frame: pd.DataFrame) -> None:
    """
    Write the DataFrame to a Parquet file at the specified path.
    """
    engine = "pyarrow"
    os.makedirs(os.path.dirname(raw_file_path), exist_ok=True)
    data_frame.to_parquet(raw_file_path, engine=engine)



def main():
    """
    1.check if data by ingest date exists in raw layer
    2.if not exists, fetch data from yfinance and write to raw layer
    3.if exist, early return .
    """
    DESIRED_TICKERS : MappingProxyType[str, dict[str, dict[str, str]]] = TICKERS
    DATA_CONTEXT = DataContext.OHLC
    LOOKBACK_PERIOD = "5y"
    
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
                    print(f"The data for {ticker_symbol} of {country} are already existed in RAW layer, skipping the fetching process...")
                    continue
                else:
                    print(f"Fetching data for {ticker_symbol} of {country} from yfinance")
                    ticker_ohlc_data_frame = ingest_ticker_ohlc(ticker_symbol, LOOKBACK_PERIOD)
                    write_parquet_ile(constructed_file_path, ticker_ohlc_data_frame)

if __name__ == "__main__":
    main()

                