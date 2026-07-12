
import os
from datetime import date
from enum import Enum
from datetime import datetime, timezone

class DataContext(Enum):
    OHLC = "ohlc"
    INFO = "info"

class FileExtention(Enum):
    PARQUET = 'parquet'
    JSON = 'json'


def construct_raw_data_file_path(ticker_synbol: str, data_context: DataContext, file_extention: FileExtention) -> str:
    """
    Construct the file path for the raw data partition based on the ticker and ingestion date.
    """
    # pattern = raw/ohlc/ingestion_date=2026-07-12/ticker=MSFT/data.parquet
    
    ingestion_date = datetime.now(timezone.utc).isoformat()
    # raw_path = f"raw/{ticker}/{data_context.value}/{ingestion_date}" # TODO: change to GCS object path later
    raw_path = f"raw/{data_context.value}/ingestion_date={ingestion_date}/ticker_symbol={ticker_synbol}" # TODO: change to GCS object path later
    raw_file = f"data.{file_extention.value}"
    fully_concatenated_file_path = os.path.join(raw_path, raw_file)
    return fully_concatenated_file_path