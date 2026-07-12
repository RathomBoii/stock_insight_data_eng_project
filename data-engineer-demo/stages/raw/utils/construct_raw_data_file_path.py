
import os
from datetime import date
from enum import Enum

class DataContext(Enum):
    OHLC = "ohlc"
    INFO = "info"
    NEWS = "news"

class FileExtention(Enum):
    PARQUET = 'parquet'
    JSON = 'json'


def construct_raw_data_file_path(ticker_synbol: str, data_context: DataContext, file_extention: FileExtention) -> str:
    """
    Construct the file path for the raw data partition based on the ticker and ingestion date.
    Hive-style partitioning: key=value folder names are auto-parsed by Spark, BigQuery, Athena, DuckDB.
    Pattern: raw/{data_context}/ticker={symbol}/ingestion_date={date}/data.{ext}
    """
    ingestion_date = date.today().isoformat()
    raw_path = f"raw/{data_context.value}/ticker={ticker_synbol}/ingestion_date={ingestion_date}"
    raw_file = f"data.{file_extention.value}"
    fully_concatenated_file_path = os.path.join(raw_path, raw_file)
    return fully_concatenated_file_path