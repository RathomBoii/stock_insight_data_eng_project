# Clean OHLC Dataflow Flex Template

This entrypoint packages the Apache Beam OHLC cleaning pipeline as a Google
Cloud Dataflow Flex Template. The batch pipeline reads raw Parquet files,
validates and enriches the OHLC bars, and writes cleaned Parquet files to the
persist stage.

## Prerequisites

- Google Cloud CLI authenticated with access to Dataflow, Cloud Build,
  Artifact Registry, and Cloud Storage
- An existing Artifact Registry Docker repository
- An existing Cloud Storage bucket for the template specification, temporary
  files, staging files, input data, and output data
- Docker, only when building the image locally

Run every command below from the repository root because we need the build context to be in repo root in order to get all required dependencies:

```bash
cd data-platform-with-clean-architecture
```

## 1. Configure the deployment

Adjust these values for the target Google Cloud environment. Artifact Registry
image hosts use the repository's **region**, not its repository name.

```bash
export GCP_PROJECT="ntt-test-data-bq-looker"
export REGION="asia-southeast1"
export ARTIFACT_REGISTRY_REPO="dataflow-demo-registry"
export PIPELINE_IMAGE_NAME="clean-ohlc-python"
export PIPELINE_IMAGE_TAG="latest"
export PIPELINE_NAME="clean-ohlc"
export GCS_BUCKET="ntt-dataflow-demo-storage"
```
```bash
export IMAGE="${REGION}-docker.pkg.dev/${GCP_PROJECT}/${ARTIFACT_REGISTRY_REPO}/${PIPELINE_IMAGE_NAME}:${PIPELINE_IMAGE_TAG}"
```
```bash
export TEMPLATE_SPEC="gs://${GCS_BUCKET}/templates/${PIPELINE_NAME}/spec.json"
export METADATA_FILE="entrypoints/clean_ohlc_from_raw_to_persist/metadata.json"
```

Set the active project:

```bash
gcloud config set project "$GCP_PROJECT"
```

## 2. Build and publish the image

Cloud Build uses the checked-in `cloudbuild.yaml` and pushes the resulting
image to Artifact Registry:

```bash
gcloud builds submit \
  --config entrypoints/clean_ohlc_from_raw_to_persist/cloudbuild.yaml \
  --substitutions "_IMAGE=${IMAGE}" \
  .
```

Alternatively, build and push with local Docker:

```bash
gcloud auth configure-docker "${REGION}-docker.pkg.dev"
```
```bash
docker build \
  --file entrypoints/clean_ohlc_from_raw_to_persist/Dockerfile \
  --tag "$IMAGE" \
  .
```
```bash
docker push "$IMAGE"
```

The build context must be the repository root because the image includes the
shared `domains`, `infrastructures`, and `usecases` packages.

## 3. Build the Flex Template specification

The template specification is a small JSON document stored in Cloud Storage.
It points Dataflow to the container image and exposes the parameters declared
in `metadata.json`. Each metadata parameter name must match an `argparse`
option in `clean_ohlc_from_raw_to_persist.py`.

```bash
gcloud dataflow flex-template build "$TEMPLATE_SPEC" \
  --image "$IMAGE" \
  --sdk-language PYTHON \
  --metadata-file "$METADATA_FILE"
```

## 4. Run the pipeline

Launch a uniquely named Dataflow job with the source glob and destination file
prefix required by the pipeline:

```bash
gcloud dataflow flex-template run "${PIPELINE_NAME}-$(date +%Y%m%d-%H%M%S)" \
  --template-file-gcs-location "$TEMPLATE_SPEC" \
  --project "$GCP_PROJECT" \
  --region "$REGION" \
  --temp-location "gs://${GCS_BUCKET}/temp" \
  --staging-location "gs://${GCS_BUCKET}/staging" \
  --parameters "source_path=gs://${GCS_BUCKET}/stages/raw/raw/ohlc/**/data.parquet,output_path=gs://${GCS_BUCKET}/stages/persist/ohlc/part"
```

Dataflow appends shard suffixes to the output prefix. A successful run produces
files similar to `part-00000-of-00001.parquet` under the persist path.

## Pipeline parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `source_path` | No | Glob matching raw OHLC Parquet files. |
| `output_path` | No | Output file prefix for cleaned Parquet shards. |

Although both parameters have local defaults, pass explicit `gs://` paths for
Dataflow runs.

## Related files

| File | Purpose |
| --- | --- |
| `clean_ohlc_from_raw_to_persist.py` | Parses template parameters and starts the Beam pipeline. |
| `Dockerfile` | Builds the Flex Template launcher image. |
| `cloudbuild.yaml` | Builds and publishes the image with Cloud Build. |
| `metadata.json` | Describes the template and its user-facing parameters. |
| `requirements.txt` | Pins the Beam SDK and runtime dependencies. |