import apache_beam as beam
import logging
import pyarrow

from apache_beam.io.parquetio import ReadFromParquet, WriteToParquet
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from collections.abc import Callable
from domains.stages.persist.rules.ohlc_bar import CalculateDailyReturn, is_valid_bar, normalize_utc
from .adapter.OHLC_bar_adapter import DictToRawOHLCBar, OHLCBarToRow
from .interfaces.execution_status import ExecutionStatus
from dataclasses import dataclass
from infrastructures.beam.beam_runner import BeamRunner

# runner="DataflowRunner",
#     project="your-gcp-project-id",
#     region="us-central1",
#     temp_location="gs://your-bucket-name/temp"

@dataclass
class CleanRawOHLCInput:
    source_path: str
    pipeline_options: PipelineOptions
    output_path: str

    # GCP arguments for Dataflow, optional for DirectRunner
    project: str | None = None
    region: str | None = None
    staging_location: str | None = None
    temp_location: str | None = None

    def __post_init__(self):
            runner = self.pipeline_options.view_as(StandardOptions).runner
            valid_runner_list = {runner_name.value for runner_name in BeamRunner}
            if runner not in valid_runner_list:
                raise TypeError(f"runner must be BeamRunner, got {runner}")

persist_OHLC_SCHEMA = pyarrow.schema([
    ("ticker", pyarrow.string()),
    ("trade_date", pyarrow.timestamp("ms", tz="UTC")),
    ("open", pyarrow.float64()),
    ("high", pyarrow.float64()),
    ("low", pyarrow.float64()),
    ("close", pyarrow.float64()),
    ("volume", pyarrow.int64()),
    ("dividends", pyarrow.float64()),
    ("stock_splits", pyarrow.float64()),
    ("ingestion_timestamp", pyarrow.timestamp("us", tz="UTC")),
    ("data_freshness", pyarrow.float64()),
    ("daily_return", pyarrow.float64()),          # nullable: first bar per ticker has none
])

class CleanRawOHLC:
    def __init__(self, props: CleanRawOHLCInput):
        self._source_path = props.source_path
        self._pipeline_options = props.pipeline_options
        self._output_path = props.output_path


    def execute(self) -> ExecutionStatus:
        try:
            with beam.Pipeline(options = self._pipeline_options) as p:
                (
                    p
                    | "Read raw"                >> ReadFromParquet(self._source_path)                    # dict per row
                    | "To raw entity"           >> beam.ParDo(DictToRawOHLCBar())                        # dict -> RawOHLCBar
                    | "Validate OHLC bar"       >> beam.Filter(is_valid_bar)                        # drop bad bars
                    | "Normalize UTC"           >> beam.Map(normalize_utc)                          # RawOHLCBar -> RawOHLCBar (UTC)
                    | "Key by ticker"           >> beam.Map(lambda bar: (bar.ticker, bar))               # (ticker, RawOHLCBar)
                    | "Group by ticker"         >> beam.GroupByKey()                                      # (ticker, [RawOHLCBar, ...])
                    | "Enrich daily return"     >> beam.ParDo(CalculateDailyReturn())                    # -> OHLCBar (enriched, both derived fields)
                    | "To row"                  >> beam.ParDo(OHLCBarToRow())                             # OHLCBar -> dict
                    | "Write persist"           >> WriteToParquet(                                        # type: ignore
                        file_path_prefix=self._output_path,
                        file_name_suffix=".parquet",
                        schema=persist_OHLC_SCHEMA,
                    )
                )
            return ExecutionStatus.SUCCEEDED
        except Exception:
            logging.exception("CleanRawOHLC pipeline failed")
            return ExecutionStatus.FAILED
