# Data Engineering Learning Guide

Use this document to resume the course with any AI assistant. The repositories,
supplied course documents, and observed Google Cloud resources are the sources
of truth. Verify them before suggesting a mutation.

## Prompt For The AI

Copy the following prompt into a new AI session:

```text
Teach me data engineering using this workspace. I am a former senior software
engineer from a TypeScript stack and plan to take the Google Cloud Professional
Data Engineer certification exam. I work in technology consulting and regularly
discover customer requirements, assess existing environments, propose enterprise
solutions, and set customer expectations. Technical data-engineering knowledge
is the core value of this course. Teach concepts and implementation deeply, then
use brief enterprise consulting situations to show how that knowledge applies
in real customer work.

Read data-engineer-learning-lessons/README.md first. Then inspect the files
named in the first incomplete lesson and verify Git status before continuing.
Do not assume this progress document is current when the repository or live
Google Cloud state disagrees with it.

Keep each response short and information-dense to reduce cognitive fatigue.
Teach one unfamiliar concept and one implementation step at a time. Use
TypeScript, Node.js, RxJS, and clean-architecture analogies when useful, but
explain where data systems behave differently. End every implementation step
and every lesson with an explicit Q&A checkpoint. Continue only after my
questions are resolved.

I perform every mutation: file edits, package installation, commits, pushes,
Google Cloud deployment, job execution, and resource deletion. You may inspect,
explain, render, lint, test, compare, and validate read-only state. Before a
cloud mutation, explain the rendered resource or command, IAM impact, expected
cost, rollback or cleanup path, and the read-only check we will use afterward.

Do not skip directly to cloud services. First connect the business requirement
to the data contract, storage layout, transformation, and operational concern.
Keep technical explanation, hands-on implementation, and validation as the main
lesson. Add a concise consulting lens only to help me imagine where the topic
appears in enterprise work. Expand customer discovery, constraints, tradeoffs,
or expectation setting only when they materially affect the technical design.
For certification preparation, distinguish durable concepts from product facts
that require current official Google Cloud documentation. The supplied training
PDFs are study sources, not proof of the current exam blueprint.
```

## Learner And Goals

- Background: former senior software engineer using TypeScript.
- Work context: enterprise technology consulting, including discovery, current-
  state assessment, requirements clarification, solution recommendation, and
  customer expectation management.
- Existing strengths: typed contracts, testing, APIs, clean architecture,
  distributed-system fundamentals, CI/CD, and production operations.
- Learning shift: data quality over request correctness, immutable history,
  event time, analytical modeling, distributed transforms, orchestration, and
  cost-aware storage and compute.
- Project: stock-market data product comparing US and China Cloud, SaaS, and
  Security companies.
- Certification goal: Google Cloud Professional Data Engineer. Exam preparation
  is a parallel track; passing the course alone does not imply exam readiness.

## Workspace Context

- `data-engineer-demo/`: local learning sandbox. It ingests Yahoo Finance OHLC,
  company profile, and news data; stores partitioned raw files; explores them
  with DuckDB; and curates OHLC data with SQL.
- `data-platform-with-clean-architecture/`: Beam implementation separated into
  domain rules, adapters, use cases, infrastructure, and entrypoints. It includes
  a Dataflow Flex Template, Cloud Build configuration, and Google Cloud Workflow.
- `data-engineer-learning-lessons/sources/`: supplied Google Cloud training
  slides covering foundations, batch, streaming, analytics, and ML.

Generated raw data, curated output, Beam output, `.venv`, caches, and Git
internals are evidence for validation but are not course source files.

## Teaching Workflow

**Session add-on (wrap every lesson, keep cognitive load low):**

- **Concept first** — briefly teach the concept of each topic before anything else.
- **Pre-quiz** — two or three short questions before learning, to surface prior
  knowledge and set a baseline (sits before step 6).
- **Post-quiz** — two or three short questions after the lab, to check retention
  (sits after step 13).
- **Low-load summary** — close with a plain-language recap of no more than three
  durable takeaways (extends step 14).

Keep each part terse and information-dense. Teach one concept and one step at a
time. The add-on applies to repository lessons and to any self-study topic.

Then the detailed workflow for every lesson:

1. Inspect Git status and the exact source files named by the lesson.
2. State one learning objective, its prerequisite, and what it unlocks next.
3. Explain one new technical concept, using one TypeScript analogy when it helps.
4. Show the concept in the repository, data, query, or execution model.
5. Ask the learner one short technical prediction or comprehension question.
6. Explain the smallest implementation step and its expected observable result.
7. Stop at a Q&A checkpoint before any mutation.
8. Let the learner make the edit or run the mutating command.
9. Review the change without rewriting the learner's explanatory comments.
10. Run the narrowest read-only validation, then explain the observed result.
11. Let the learner stage, commit, push, deploy, or clean up when applicable.
12. Briefly connect the evidence to one realistic enterprise use when useful.
13. Add a discovery question, tradeoff, expectation, or client-facing statement
  only when it helps apply or communicate the technical decision.
14. Summarize no more than three durable technical takeaways.
15. Stop at a lesson Q&A checkpoint and update Course Progress only after the
    learner confirms the lesson is complete.

Do not combine setup, implementation, deployment, and exploration into one
response. A lesson may take several sessions. Prefer a visible result such as a
query result, Parquet schema, Beam graph, Dataflow job state, or query plan over
an abstract explanation.

## Enterprise Application Lens

Technical mastery remains primary. The consulting lens exists to answer:

> Where would I use this knowledge in enterprise customer work?

Use the following sequence only when the current technical topic reaches an
architecture or customer decision:

```text
Customer outcome
    -> current environment and constraints
    -> clarified functional and non-functional requirements
    -> options and tradeoffs
    -> recommendation with assumptions
    -> expectation, risk, validation, and next decision
```

When relevant, teach the learner how to:

- distinguish the stated request from the underlying business outcome;
- ask precise discovery questions without overwhelming the customer;
- identify scale, latency, availability, security, compliance, integration,
  operating-model, skills, timeline, and budget constraints;
- separate verified facts, customer statements, assumptions, and unknowns;
- avoid recommending a Google Cloud product before understanding the workload;
- present viable options and explain why one is recommended;
- set expectations about scope, cost, performance, dependencies, migration,
  operational ownership, and residual risk;
- translate evidence for engineers, architects, product owners, security,
  operations, and executives.

Do not turn each technical step into consulting role-play. Keep this section
brief unless the learner asks for more detail or the design depends on customer
requirements. When useful, include only one practical connection, for example:

- one high-value discovery question and why its answer changes the design;
- a fact-versus-assumption table with no more than three rows;
- a short decision statement with one rejected alternative;
- one expectation statement about scope, cost, performance, or ownership;
- one risk with impact, evidence, mitigation, and responsible owner.

## Mutation And Cloud Safety

- Never include unrelated dirty files in a lesson commit.
- Never expose credentials, tokens, service-account keys, or private data.
- Inspect a command and its target project, region, identity, and resource name
  before the learner runs it.
- Prefer least-privilege service accounts and application default credentials;
  do not create long-lived keys for convenience.
- Establish budgets or cost expectations before Dataproc, Dataflow, BigQuery,
  Bigtable, Composer, Data Fusion, or Vertex AI labs.
- Give every temporary cloud lab a cleanup checklist and verify deletion.
- For destructive data changes, verify a reproducible source or backup first.
- Treat an empty successful pipeline as a possible failure. Validate input count,
  output count, rejected records, freshness, and schema.

## Source Audit

All human-authored Python, SQL, Markdown, YAML, JSON, Docker, packaging, and
ignore files in both repositories were inspected on 2026-07-26. The empty raw
data notebook and four empty explorer scripts contain no learning content yet.

All 26 supplied PDFs were text-extracted successfully with no empty pages. The
editable `M1.0_Introduction.docx` was also extracted and is substantively the
course introduction represented by its PDF. The PDFs form this four-part path:

| Module | Supplied sources | Durable focus |
| --- | --- | --- |
| 1. Foundations | `M1.0`-`M1.4` | Data engineering role, lakes, warehouses, Cloud Storage, BigQuery, governance |
| 2. Batch | `M2.0`-`M2.5` | Batch patterns, Dataproc/Spark, Beam/Dataflow, Data Fusion, Composer |
| 3. Streaming | `M3.1`-`M3.6` | Pub/Sub, event time, windows, watermarks, Dataflow, BigQuery, Bigtable |
| 4. Analytics and ML | `M4.0`-`M4.7` | Managed ML APIs, notebooks, pipelines, BigQuery ML, Vertex AI AutoML |

`T-GCPDE-I_DataSheet_RGB.pdf` is an eight-page 2022 training-course datasheet.
It describes the four-day course and its modules; it is not a current official
Professional Data Engineer exam guide and does not provide authoritative exam
domain weights. Before certification review, compare this curriculum with the
current official exam guide and product documentation.

Some slides use practices or product positioning that may have changed. Verify
current guidance for Dataproc Serverless, the BigQuery Storage Write API,
Dataform and Dataplex, Cloud Composer versions, Vertex AI Pipelines versus direct
Kubeflow usage, Vertex AI AutoML naming, IAM, quotas, pricing, and regional
availability.

## Architecture Under Study

```text
Business questions and data-quality contract
                    |
                    v
Yahoo Finance -> immutable raw partitions (Parquet / JSON)
                    |
                    +-> DuckDB exploration and SQL curation
                    |
                    +-> Beam domain transforms
                              |
                              v
                    cleaned persist Parquet
                              |
                              v
                 BigQuery analytical model
                              |
                  +-----------+-----------+
                  |                       |
                 BI                 analytics / ML

Cloud path: Cloud Storage -> Dataflow Flex Template -> Cloud Storage / BigQuery
                                ^
                                |
                    Cloud Build + Workflows
```

## Curriculum

The lessons are incremental. Repository-backed lessons use existing code.
Extension lessons add a small exercise only after its design is understood.

### Lesson 1: Data Product And Quality Contract - Next

**Mode:** repository-backed, read-only.

**Sources:**

- `data-engineer-demo/README.md`
- `data-engineer-learning-lessons/sources/M1.1_Introduction_to_Data_Engineering.pdf`

**Learn:** translate a business question into datasets, grain, timestamps,
freshness, null semantics, point-in-time correctness, and acceptance criteria.
Compare an API contract with a data contract: an API validates one interaction;
a data contract must also protect history and analytical meaning.

**Lab:** trace one dashboard question to the required OHLC fields and identify
the grain of one raw OHLC record.

**Completion evidence:** the learner can state the grain, event timestamp,
ingestion timestamp, and three quality invariants without looking them up.

**First user action:** read only the `Data Requirements` and `data-quality
contract` sections of `data-engineer-demo/README.md`, then answer: "What is one
OHLC row about, and which timestamp says when the market event happened?"

### Lesson 2: Raw Lake And Partition Design - Not Started

**Mode:** repository-backed.

**Sources:** `M1.2_Building_a_Data_Lake.pdf`, `TICKERS.py`,
`construct_raw_data_file_path.py`, `check_existing_raw_data.py`, and
`write_json_file.py`.

**Learn:** schema-on-read, immutable raw data, object naming, Hive-style
partitioning, idempotence, small-file risk, and ingestion date versus event date.

**Lab:** predict and then inspect the path produced for one ticker and date.

### Lesson 3: Batch Ingestion And Source Boundaries - Not Started

**Mode:** repository-backed.

**Sources:** `M2.1_Introduction_to_Building_Batch_Data_Pipelines.pdf`,
`ingest_all.py`, `ingest_stock_ohlc.py`, `ingest_stock_info.py`, and
`ingest_stock_news.py`.

**Learn:** bounded data, extract/load boundaries, retries, partial failure,
source-specific schemas, and why missing values are not zero.

**Lab:** run one ticker through the smallest local ingestion path and validate
the file, schema, timestamps, and row count.

### Lesson 4: Parquet And Analytical File Layout - Not Started

**Mode:** repository-backed.

**Sources:** `parquet_compression_notes.md`, `ticker_search.py`, and
`explore.sql`.

**Learn:** row versus column storage, schema, predicate and column pruning,
compression, partition pruning, and the small-file tradeoff.

**Lab:** inspect Parquet metadata and compare a narrow analytical query with a
full-row scan.

### Lesson 5: Curation With SQL - Not Started

**Mode:** repository-backed.

**Sources:** `M1.3_Building_a_Data_Warehouse.pdf`, `explore.sql`, and
`stages/curate/curate_ohlc.py`.

**Learn:** raw versus curated responsibilities, validation, deduplication,
window functions, data grain, and deterministic ordering.

**Lab:** follow one ticker through `raw`, `valid`, `deduped`, and daily-return
calculation; reconcile input, rejected, duplicate, and output counts.

### Lesson 6: Python Data Work For A TypeScript Engineer - Not Started

**Mode:** repository-backed.

**Sources:** `pandas-cleaning-data-example/main.py`, raw and persist entities,
and OHLC domain rules.

**Learn:** Python typing, dataclasses, iterators, null/NaN behavior, timezone
objects, Pandas vectorization, and runtime schema validation. Compare TypeScript
types erased at runtime with Python annotations plus explicit data schemas.

**Lab:** test one pure OHLC validation or normalization rule with valid and
invalid records.

### Lesson 7: Apache Beam Mental Model - Not Started

**Mode:** repository-backed.

**Sources:** `M2.3_Serverless_Data_Processing_with_Dataflow.pdf`,
`apache-beam/python_operator_overloading.md`, and
`apache-beam/simple_pipeline_creation_example.py`.

**Learn:** pipeline, runner, PCollection, PTransform, boundedness, fusion,
serialization, workers, schemas, and sinks. Use RxJS as a syntax bridge while
noting that Beam constructs a portable distributed execution graph.

**Lab:** predict each element after `Create` and `Filter`, run DirectRunner, and
inspect the Parquet shards rather than forcing a single production shard.

### Lesson 8: Clean Architecture For Data Pipelines - Not Started

**Mode:** repository-backed.

**Sources:** clean-architecture entities, OHLC rules, adapter,
`usecases/clean_ohlc.py`, and `infrastructures/beam/beam_runner.py`.

**Learn:** domain purity, ports and adapters, Beam DoFns, dependency direction,
and where schemas belong. Compare the layout with a TypeScript hexagonal service.

**Lab:** trace one dictionary from Parquet through raw entity, rules, persist
entity, row adapter, and output schema.

### Lesson 9: Correct Distributed Time-Series Transforms - Not Started

**Mode:** repository-backed hardening exercise.

**Sources:** `calculate_daily_return.py`, `calculate_data_freshness.py`,
`normalize_utc.py`, `is_valid_bar.py`, and `usecases/clean_ohlc.py`.

**Learn:** keying, grouping, ordering, shuffle cost, event time, time zones,
first-record nulls, deterministic calculation, and data-quality side outputs.

**Lab:** write focused tests before correcting any discovered ticker mapping,
ordering, timestamp, or path-contract defect.

### Lesson 10: Dataflow Flex Template Packaging - Not Started

**Mode:** repository-backed; local validation before cloud mutation.

**Sources:** clean-architecture root `README.md`, entrypoint `README.md`,
`clean_ohlc_from_raw_to_persist.py`, `setup.py`, `requirements.txt`,
`Dockerfile`, `metadata.json`, and `cloudbuild.yaml`.

**Learn:** launcher container versus worker environment, package staging,
pipeline options, template parameters, Artifact Registry, architecture targets,
and immutable image tags.

**Lab:** validate imports and parameter contracts locally, inspect the image and
template build commands, then let the learner build only after cost/IAM review.

### Lesson 11: Orchestration And Operations - Not Started

**Mode:** repository-backed plus design comparison.

**Sources:** `M2.4_Manage_Data_Pipelines_with_Cloud_Data_Fusion_and_Cloud_Composer.pdf`
and `workflow.yaml`.

**Learn:** orchestration versus processing, control plane versus data plane,
parameters, retries, backfills, idempotent output, observability, and choosing
Workflows, Composer, Data Fusion, or a scheduler.

**Lab:** dry-read the Workflow expression evaluation and verify its source and
output paths against the ingestion contract before any deployment.

### Lesson 12: BigQuery Storage And Modeling - Not Started

**Mode:** extension lesson.

**Sources:** `M1.3_Building_a_Data_Warehouse.pdf`,
`M3.5_Advanced_BigQuery_Functionality_and_Performance.pdf`, curated OHLC schema,
and business requirements.

**Learn:** table grain, facts and dimensions, denormalization, nested fields,
partitioning, clustering, materialized views, query plans, bytes scanned, and
cost controls.

**Lab:** design and review DDL for OHLC facts and ticker dimensions before the
learner creates a dataset or loads data.

### Lesson 13: Spark And Dataproc Tradeoffs - Not Started

**Mode:** source-led comparison with a small optional lab.

**Sources:** `M2.2_Executing_Spark_on_Dataproc.pdf`, DuckDB curation, and Beam
pipeline.

**Learn:** Spark lazy DAGs, partitions, shuffle, caching, cluster versus
serverless execution, and when DuckDB, BigQuery SQL, Beam/Dataflow, or Spark is
the simpler tool.

**Lab:** express the same validation and daily-return job conceptually in SQL,
Beam, and Spark, then justify one choice from scale and operational constraints.

### Lesson 14: Pub/Sub And Streaming Contracts - Not Started

**Mode:** extension lesson.

**Sources:** `M3.1_Introduction.pdf` and
`M3.2_Serverless_Messaging_with_Pub_Sub.pdf`.

**Learn:** events, topics, subscriptions, acknowledgements, redelivery,
ordering, dead-letter handling, schemas, idempotent consumers, and delivery
semantics.

**Lab:** design a versioned stock-event envelope and a duplicate-safe consumer;
create cloud resources only after IAM, quota, cost, and cleanup review.

### Lesson 15: Event Time And Dataflow Streaming - Not Started

**Mode:** extension lesson.

**Sources:** `M3.3_Dataflow_Streaming_Features.pdf` and Beam code from Lessons 7-9.

**Learn:** event time versus processing time, windows, watermarks, triggers,
allowed lateness, state, timers, accumulation modes, and replay.

**Lab:** use a tiny local TestStream with on-time, late, and duplicate events;
predict pane outputs before running it.

### Lesson 16: Streaming Sinks And Serving Choices - Not Started

**Mode:** extension lesson.

**Sources:** `M3.4_High-Throughput_BigQuery_and_Bigtable_Streaming_Features.pdf`
and `M3.5_Advanced_BigQuery_Functionality_and_Performance.pdf`.

**Learn:** analytical versus low-latency key access, Storage Write API concepts,
Bigtable row-key design and hotspots, batching, backpressure, quotas, and cost.

**Lab:** choose BigQuery or Bigtable for three stock-data access patterns and
defend each choice with latency, query shape, consistency, and cost.

### Lesson 17: Analytics And ML Enablement - Not Started

**Mode:** extension lesson; secondary to core data engineering.

**Sources:** `M4.1`-`M4.7`, the empty exploration notebook, news ingestion, and
the curated OHLC output.

**Learn:** reproducible notebooks, feature leakage, train/evaluate boundaries,
BigQuery ML, managed APIs for unstructured news, Vertex AI AutoML, and production
ML pipeline responsibilities. Reinterpret older Kubeflow material using current
Vertex AI guidance.

**Lab:** build an explainable BigQuery ML baseline or news-enrichment experiment
only after defining point-in-time-safe features and evaluation metrics.

### Lesson 18: Reliability, Security, Cost, And Exam Review - Not Started

**Mode:** synthesis and gap closure.

**Sources:** all module summaries, `T-GCPDE-I_DataSheet_RGB.pdf`, current official
Professional Data Engineer exam guide, deployment files, and all lab evidence.

**Learn:** data SLOs, lineage, catalog and governance, IAM, encryption, sensitive
data controls, regional design, disaster recovery, monitoring, autoscaling,
quotas, cost optimization, migration, and service selection under constraints.

**Lab:** perform a scenario review and architecture defense, then create a gap
list from the current official exam guide. Do not memorize obsolete slide facts.

## Certification Coverage

The current repository is strongest in batch processing and Dataflow packaging.
The supplied sources broaden the theory, but several exam-relevant capabilities
need new labs and current documentation.

| Capability | Current evidence | Main lessons |
| --- | --- | --- |
| Design data processing systems | Business contract, layered storage, clean architecture | 1, 2, 8, 12, 13 |
| Ingest and process batch data | Yahoo ingestion, DuckDB, Beam, Dataflow | 3-11 |
| Design storage and analytics | Parquet and SQL; BigQuery lab still required | 2, 4, 5, 12 |
| Build streaming systems | Source theory only; implementation required | 14-16 |
| Maintain and automate workloads | Cloud Build, Flex Template, Workflows; monitoring gaps | 10, 11, 18 |
| Security and governance | Mostly absent from code | 12, 14, 18 |
| Reliability and cost optimization | Partial deployment evidence; explicit labs required | 10-13, 16, 18 |
| Enable analytics and ML | Requirements and source theory; labs required | 12, 17 |

Before Lesson 18, retrieve the current official exam guide and map every stated
objective to `Demonstrated`, `Explained`, or `Gap`. Do not infer current domain
weights from the supplied 2022 training datasheet.

## Known Repository Gaps To Use As Lessons

These are investigation targets, not pre-approved fixes:

- No automated tests currently cover domain rules, adapters, or pipeline output.
- The raw explorer notebook and explorer scripts are empty.
- BigQuery and GCS infrastructure directories are placeholders.
- News, ticker, and profile entities are not wired into clean-architecture use
  cases.
- Local and Workflow source-path conventions must be reconciled with the actual
  raw partition layout before deployment.
- The OHLC adapter's ticker mapping must be verified against actual Parquet
  fields and Hive partition values.
- The daily-return transform must prove deterministic per-ticker ordering.
- Cloud identifiers and a fixed ingestion date are embedded in `workflow.yaml`.
- The root sandbox lacks a declared dependency manifest.
- A successful job can still process zero records; count and freshness
  validation are not yet first-class pipeline outputs.

Each gap should be approached as: reproduce or inspect, state a falsifiable
hypothesis, add a focused test or query, make the smallest learner-owned change,
and validate the observable result.

## Course Progress

| Lesson | Status | Evidence |
| --- | --- | --- |
| 1. Data Product And Quality Contract | Next | None yet |
| 2. Raw Lake And Partition Design | Not Started | None |
| 3. Batch Ingestion And Source Boundaries | Not Started | None |
| 4. Parquet And Analytical File Layout | Not Started | None |
| 5. Curation With SQL | Not Started | None |
| 6. Python Data Work For A TypeScript Engineer | Not Started | None |
| 7. Apache Beam Mental Model | Not Started | None |
| 8. Clean Architecture For Data Pipelines | Not Started | None |
| 9. Correct Distributed Time-Series Transforms | Not Started | None |
| 10. Dataflow Flex Template Packaging | Not Started | None |
| 11. Orchestration And Operations | Not Started | None |
| 12. BigQuery Storage And Modeling | Not Started | None |
| 13. Spark And Dataproc Tradeoffs | Not Started | None |
| 14. Pub/Sub And Streaming Contracts | Not Started | None |
| 15. Event Time And Dataflow Streaming | Not Started | None |
| 16. Streaming Sinks And Serving Choices | Not Started | None |
| 17. Analytics And ML Enablement | Not Started | None |
| 18. Reliability, Security, Cost, And Exam Review | Not Started | None |

## Resume Checklist

At the start of a new session, report only:

1. Git status for files relevant to the first incomplete lesson.
2. The first incomplete lesson and its objective.
3. Whether repository or cloud evidence disagrees with Course Progress.
4. The single next learner action.

Do not begin the next implementation step until the learner's Q&A checkpoint is
resolved.
