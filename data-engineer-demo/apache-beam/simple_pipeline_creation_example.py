"""
This is the example Apache Beam code example to demonstrate
1) How to create pipeline with pipelineOptions
2) How to tell Beam to use desired runner
3) How to simple do the data processing, in this case is simple clean data
4) How to write the processed data out to a parquet file
"""

import apache_beam as beam
import pyarrow
from apache_beam.options.pipeline_options import PipelineOptions

# WriteToParquet needs an explicit pyarrow schema; every element must match it
PLAYER_SCHEMA = pyarrow.schema([
    ("name", pyarrow.string()),
    ("class", pyarrow.string()),
    ("level", pyarrow.int64()),
])

# Create Pipeline options
pipelineOptions = PipelineOptions(
    runner='DirectRunner', # default is already be 'DirectRunner'
    direct_num_workers=2, # How many CPU reserved on the runner
    direct_running_mode='multi_processing',
)


# Create filter function
def filter_high_level_player(player):
    """
    Filter the player with level > 10

    Note:
        This receives a single player dict, not the whole list. The list passed to
        beam created is only how we hand the initial data to Beam in Python - Beam
        turns it into a PCollection of 5 individual elements. Transforms like Filter,
        Map and ParDo are applied once per element, so Beam owns the iteration and
        can spread the elements across workers. Writing our own loop here would
        defeat that.
    """
    return player['level'] > 10

# Create Beam pipeline
# `with` syntax manage resource by automatically setup and clean up resources

with beam.Pipeline(options = pipelineOptions) as p:
    """
    Beam pipeline pattern is 
    1. Create Transform to process data (it's a python function)
    2. Create pipeline which encapsulate the data processing logic
    3. Create the PCollection from input data
    4. Pass the PCollection to a Transform
    5. Write the output to a sink (in this case is parquet file)
    
    Note:
        The process 3-4 is called "Apply Transform" which have the syntax pattern
        utilize the python operator overload like this below:
            pipeline | label (the transform's name) >> transform (the transform function)

    Term of use of `|` and `>>` symbol (Which underlying mechanism is operator overloading)
        `|` moves the data. `>>` only sticks a name on the transform to its right.

        The line below reads as if `|` is doing the labelling, because the `|` sits
        right next to the label. It is not. `>>` binds tighter than `|` (same way `*`
        binds tighter than `+`, so `2 + 3 * 4` means `2 + (3 * 4)`), so:

            p | "RPG Player" >> beam.Create([...])

        actually groups as:

            p | ("RPG Player" >> beam.Create([...]))

        The inner part runs first, and there is no `p` inside it - no pipeline, no
        PCollection, nothing to apply to. It only builds a _NamedPTransform holding
        (beam.Create([...]), "RPG Player"): a transform wearing a name tag. Nothing
        has run yet. Then the outer `p | <labeled transform>` is the actual apply,
        and that is what returns a PCollection.

        Proof that `>>` is optional but `|` is not:

            p | beam.Create([...]) | beam.Filter(f)   # works, Beam auto-names the steps
            "RPG Player" >> beam.Create([...])        # does nothing, object thrown away

        Labels only exist to make the pipeline graph and error messages readable.

        The whole chain is a single expression, so it must be wrapped in parentheses
        to span multiple lines.
    """
    # Each `|` takes what is on its left (the pipeline, then the PCollection produced
    # by the step above it) and applies the labeled transform on its right.
    (
        p
        | "RPG Player" >> beam.Create([
            {"name": "Arthor", "class": "Warrior", "level": 10},
            {"name": "Mania", "class": "Mage", "level": 20},
            {"name": "Arathon", "class": "Rogue", "level": 15},
            {"name": "Ladven", "class": "Cleric", "level": 5},
            {"name": "Pondulaz", "class": "Paladin", "level": 25},
        ])
        | "Filter high level player" >> beam.Filter(filter_high_level_player)
        # WriteToParquet is a sink: it eats the PCollection element by element and
        # buffers the writes itself, so there is no need to aggregate the elements
        # into a list first. num_shards=1 forces a single output file, which kills
        # the parallel write - fine for this demo, bad for real volume.
        | "Write to parquet" >> beam.io.WriteToParquet( # type: ignore
            file_path_prefix='output/high_level_player',
            file_name_suffix='.parquet',
            schema=PLAYER_SCHEMA
            # num_shards=1,
        )
    )