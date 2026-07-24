# Flex Template image for the clean_ohlc_from_raw_to_persist pipeline.
# IMPORTANT: build with context = repo root so shared packages
# (domains/, usecases/, infrastructures/) are visible:
#   docker build -f entrypoints/clean_ohlc_from_raw_to_persist/Dockerfile -t IMAGE .

# Stage 1: grab Google's Flex Template launcher binary.
FROM gcr.io/dataflow-templates-base/python312-template-launcher-base:latest AS launcher

# Stage 2: run on the matching Beam SDK image so launcher Beam == worker Beam.
FROM apache/beam_python3.12_sdk:2.75.0

ARG WORKDIR=/template
WORKDIR ${WORKDIR}

COPY --from=launcher /opt/google/dataflow/python_template_launcher /opt/google/dataflow/python_template_launcher

# Context is repo root, so this copies the whole project tree.
COPY . ${WORKDIR}/

# Put the repo root on the launcher import path. Worker imports are provided by
# the package staged from FLEX_TEMPLATE_PYTHON_SETUP_FILE below.
ENV PYTHONPATH="${WORKDIR}"

# Paths are relative to WORKDIR (= repo root inside the image).
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/entrypoints/clean_ohlc_from_raw_to_persist/clean_ohlc_from_raw_to_persist.py"
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/entrypoints/clean_ohlc_from_raw_to_persist/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r ${FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE}

ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]
