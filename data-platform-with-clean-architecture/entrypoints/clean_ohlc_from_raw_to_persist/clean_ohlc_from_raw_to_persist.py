import argparse
import sys

from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from infrastructures.beam.beam_runner import BeamRunner
from usecases.clean_ohlc import CleanRawOHLC, CleanRawOHLCInput
from usecases.interfaces.execution_status import ExecutionStatus


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean raw OHLC bars into the persist stage.")
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

    # Pipeline-specific args are ours; everything else (--runner, --project,
    # --region, --temp_location, --staging_location, and all Dataflow service
    # options) is handled by Beam via PipelineOptions. The Flex Template
    # launcher passes those in on the command line at run time.
    args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(pipeline_args)

    # Local ergonomics: when no --runner is supplied (bare local run), default
    # to DirectRunner. On Dataflow the Flex Template launcher passes
    # --runner DataflowRunner, which takes precedence and is left untouched.
    if pipeline_options.view_as(StandardOptions).runner is None:
        pipeline_options.view_as(StandardOptions).runner = BeamRunner.DIRECT.value

    props = CleanRawOHLCInput(
        source_path=args.source_path,
        pipeline_options=pipeline_options,
        output_path=args.output_path,
    )

    pipeline_execution_status = CleanRawOHLC(props).execute()
    print(f"clean_ohlc: {pipeline_execution_status.value}")

    return 0 if pipeline_execution_status is ExecutionStatus.SUCCEEDED else 1


if __name__ == "__main__":
    sys.exit(main())
