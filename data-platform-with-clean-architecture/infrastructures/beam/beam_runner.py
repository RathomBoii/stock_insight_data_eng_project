from enum import Enum

class BeamRunner(Enum):
        DIRECT = "DirectRunner"
        DATAFLOW = "DataflowRunner"
        SPARK   = "SparkRunner"
        