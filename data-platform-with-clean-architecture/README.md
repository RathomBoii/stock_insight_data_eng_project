# Data Platform with Clean Architecture

## Packaging Python code for Dataflow workers

The Dataflow pipeline originally failed after successfully pulling and starting
the Flex Template image:

```text
ModuleNotFoundError: No module named 'domains'
```

The fix includes:

- Added [`setup.py`](setup.py) to package:
  - [`domains`](domains/)
  - [`usecases`](usecases/)
  - [`infrastructures`](infrastructures/)
- Updated the pipeline
  [`Dockerfile`](entrypoints/clean_ohlc_from_raw_to_persist/Dockerfile) so
  Dataflow stages that package to workers.
- Added `setuptools` to the pipeline
  [`requirements.txt`](entrypoints/clean_ohlc_from_raw_to_persist/requirements.txt).

### TypeScript analogy

- `setup.py` is roughly the Python equivalent of package metadata in
  `package.json`.
- The Flex Template launcher container is like a CI build container.
- Dataflow workers are separate runtime machines.
- Copying source into the launcher container does not automatically install it
  on worker machines.
- `FLEX_TEMPLATE_PYTHON_SETUP_FILE` tells Dataflow to bundle and install the
  local Python project on every worker.

When adding another Dataflow pipeline that imports local project modules, make
sure those modules are included by `setup.py` and configure the pipeline image
with `FLEX_TEMPLATE_PYTHON_SETUP_FILE`.