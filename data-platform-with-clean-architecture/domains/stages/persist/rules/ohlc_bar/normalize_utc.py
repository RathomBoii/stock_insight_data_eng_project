from datetime import timezone
from domains.stages.persist.entities.raw_ohlc_bar import RawOHLCBar, RawOHLCBarInput


def normalize_utc(bar: RawOHLCBar) -> RawOHLCBar:
    """§5.1 contract: every timestamp UTC. Raw is tz=America/New_York."""
    return RawOHLCBar(RawOHLCBarInput(
        ticker=bar.ticker,
        trade_date=bar.trade_date.astimezone(timezone.utc),
        open=bar.open,
        high=bar.high,
        low=bar.low,
        close=bar.close,
        volume=bar.volume,
        dividends=bar.dividends,
        stock_splits=bar.stock_splits,
        ingestion_timestamp=bar.ingestion_timestamp,
    ))
