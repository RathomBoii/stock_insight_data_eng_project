"""
Daily return = (today's closing price - yesterday's closing price) / yesterday's closing price

Enrich transition: RawOHLCBar -> OHLCBar.
Needs neighbours (previous bar), so it runs after GroupByKey per ticker.
"""
import apache_beam as beam

from typing import Iterable, Iterator, Tuple
from domains.stages.persist.entities.raw_ohlc_bar import RawOHLCBar
from domains.stages.persist.entities.ohlc_bar import OHLCBar, OHLCBarInput

# ! Note both fields data_freshness and daily_return must be set at the same time, so we need to import this function too
from .calculate_data_freshness import calculate_data_freshness


class CalculateDailyReturn(beam.DoFn):

    def process(self, element: Tuple[str, Iterable[RawOHLCBar]]) -> Iterator[OHLCBar]:
        """
        1. receive (ticker, [RawOHLCBar, ...])
        2. sort by trade_date
        3. loop: daily_return vs previous close, data_freshness per bar
        4. yield enriched OHLCBar
        """
        key, records = element

        sorted_records = sorted(records, key=lambda bar: bar.trade_date)

        previous_bar = None
        for bar in sorted_records:
            # Ternary operator
            #  variable = value_if_true if condition else value_if_false
            daily_return = (
                (bar.close - previous_bar.close) / previous_bar.close
                if previous_bar is not None
                else None
            )

            yield OHLCBar(OHLCBarInput(
                ticker=bar.ticker,
                trade_date=bar.trade_date,
                open=bar.open,
                high=bar.high,
                low=bar.low,
                close=bar.close,
                volume=bar.volume,
                dividends=bar.dividends,
                stock_splits=bar.stock_splits,
                ingestion_timestamp=bar.ingestion_timestamp,
                data_freshness=calculate_data_freshness(bar.ingestion_timestamp, bar.trade_date),
                daily_return=daily_return,
            ))

            previous_bar = bar
