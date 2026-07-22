from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawOHLCBarInput:
    ticker: str
    trade_date: datetime      # UTC after normalize
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: float
    stock_splits: float
    ingestion_timestamp: datetime


class RawOHLCBar:
    """Bar as ingested. No derived fields yet. Enriched into OHLCBar downstream."""

    def __init__(self, props: RawOHLCBarInput):
        self._ticker = props.ticker
        self._trade_date = props.trade_date
        self._open = props.open
        self._high = props.high
        self._low = props.low
        self._close = props.close
        self._volume = props.volume
        self._dividends = props.dividends
        self._stock_splits = props.stock_splits
        self._ingestion_timestamp = props.ingestion_timestamp

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def trade_date(self) -> datetime:
        return self._trade_date

    @property
    def open(self) -> float:
        return self._open

    @property
    def high(self) -> float:
        return self._high

    @property
    def low(self) -> float:
        return self._low

    @property
    def close(self) -> float:
        return self._close

    @property
    def volume(self) -> int:
        return self._volume

    @property
    def dividends(self) -> float:
        return self._dividends

    @property
    def stock_splits(self) -> float:
        return self._stock_splits

    @property
    def ingestion_timestamp(self) -> datetime:
        return self._ingestion_timestamp
