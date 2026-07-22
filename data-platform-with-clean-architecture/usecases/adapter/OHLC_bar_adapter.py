import apache_beam as beam
from datetime import datetime
from domains.stages.persist.entities.raw_ohlc_bar import RawOHLCBar, RawOHLCBarInput
from domains.stages.persist.entities.ohlc_bar import OHLCBar


class DictToRawOHLCBar(beam.DoFn):
    """Raw parquet row (dict) -> raw domain entity. Adapter = translation only."""
    def process(self, row: dict):
        yield RawOHLCBar(RawOHLCBarInput(
            ticker=row["name"],               # ticker symbol; the raw dir partitions on ticker= but that key is not a column
            trade_date=row["Date"],           # tz=America/New_York here, rule fixes it
            open=row["Open"],
            high=row["High"],
            low=row["Low"],
            close=row["Close"],
            volume=row["Volume"],
            dividends=row["Dividends"],
            stock_splits=row["Stock Splits"],
            ingestion_timestamp=datetime.fromisoformat(row["ingestion_timestamp"]),
        ))


class OHLCBarToRow(beam.DoFn):
    """Enriched domain entity -> dict for the parquet sink."""
    def process(self, bar: OHLCBar):
        yield {
            "ticker": bar.ticker,
            "trade_date": bar.trade_date,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
            "dividends": bar.dividends,
            "stock_splits": bar.stock_splits,
            "ingestion_timestamp": bar.ingestion_timestamp,
            "data_freshness": bar.data_freshness,
            "daily_return": bar.daily_return,
        }
