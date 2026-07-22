import argparse
import sys

from apache_beam.options.pipeline_options import PipelineOptions
from domains.stages.persist.rules.ohlc_bar import is_valid_bar, normalize_utc
from infrastructures.beam.beam_runner import BeamRunner
from usecases.clean_ohlc import CleanRawOHLC, CleanRawOHLCInput
from usecases.interfaces.execution_status import ExecutionStatus


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean raw OHLC bars into the persist stage.")
    parser.add_argument(
        "--runner",
        default=BeamRunner.DIRECT.name,
        choices=[runner.name for runner in BeamRunner],
        help="Beam runner to execute the pipeline with.",
    )
    parser.add_argument(
        "--source_path",
        default="stages/raw/raw/ohlc/**/data.parquet",
        help="Glob of the raw parquet files to read.",
    )
    parser.add_argument(
        "--output_path",
        default="cleaned/stages/persist/ohlc/part",
        help="File path prefix for the persist parquet output.",
    )
    parser.add_argument(
        "--project",
        default=None,
        help="GCP project ID (required for DataflowRunner).",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="GCP region (required for DataflowRunner).",
    )
    parser.add_argument(
        "--staging_location",
        default=None,
        help="GCS path for staging files (required for DataflowRunner: where your code goes. Beam uploads the pipeline JAR/pickled code and dependencies here so workers can download them at startup. Written once, at job submit).",
    )
    parser.add_argument(
        "--temp_location",
        default=None,
        help="GCS path for temporary files (required for DataflowRunner: where data goes during the run. Shuffle spill, intermediate files, and in-progress sink writes. WriteToParquet writes here first, then renames to your --output-prefix on success).",
    )
    
    args = parser.parse_args()

    runner = BeamRunner[args.runner]

    props = CleanRawOHLCInput(
        source_path=args.source_path,
        pipeline_options=PipelineOptions(flags=[], runner=runner.value),
        output_path=args.output_path,
        region=args.region,
        project=args.project,
        staging_location=args.staging_location,
        temp_location=args.temp_location,
    )

    pipeline_execution_status = CleanRawOHLC(props).execute()
    print(f"clean_ohlc: {pipeline_execution_status.value}")

    return 0 if pipeline_execution_status is ExecutionStatus.SUCCEEDED else 1


if __name__ == "__main__":
    sys.exit(main())
