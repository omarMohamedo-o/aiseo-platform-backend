# dataset/

Versioned datasets used for ML training and evaluation (search-intent
classification, question classification, answer evaluation, etc.).

Each dataset must be identifiable via a `DatasetVersion` (see
`docs/architecture.md#62-data-versioning`): `dataset_id`, `version`,
`source`, `content_hash`, `creation_time`, `schema_version`. A model's
MLflow run must reference the exact dataset version it was trained/evaluated
on. Do not overwrite a dataset file in place — write a new version.

Empty in Phase 1; populated starting Phase 7 (ML).
