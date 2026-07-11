
import os
from datetime import date
from enum import Enum

class DataContext(Enum):
    OHLC = "OHLC"
    INFO = "INFO"


def construct_raw_data_file_path(ticker: str, data_context: DataContext) -> str:
    """
    Construct the file path for the raw data partition based on the ticker and ingestion date.
    """
    ingestion_date = date.today().isoformat()
    raw_path = f"raw/{ticker}/{data_context.value}/{ingestion_date}" # TODO: change to GCS object path later
    raw_file = os.path.join(raw_path, f"{ticker}_{ingestion_date}.parquet")
    return raw_file