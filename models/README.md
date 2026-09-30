# models/

Exported, versioned **ONNX** model artifacts served at inference time via
`aiseo.adapters.ml.onnx_model_provider.OnnxModelProvider` (ONNX Runtime,
`CPUExecutionProvider` by default; swap execution providers or move serving
to a C++/ONNX Runtime process for high-throughput production workloads
without changing the `ModelProvider` port).

Models are **trained and evaluated offline** (see `notebooks/` and
`docs/architecture.md#57-mlflow`), tracked and versioned in **MLflow**, and
only the exported `.onnx` file + its registered model name/version are
placed here for serving.

Naming convention: `{model_name}_v{version}.onnx`, e.g.
`intent_classifier_v1.onnx`.

`intent_classifier_v1.onnx` in this repo is a minimal placeholder (a single
linear/Gemm layer) used purely to exercise the `ModelProvider` port and its
tests end-to-end — it is not a trained model.
