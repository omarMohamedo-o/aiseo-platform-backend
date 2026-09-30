"""Model-serving port. Business code depends on this, never on onnxruntime,
sklearn, or MLflow's SDK types directly.

Defined as a `Protocol` (structural typing) rather than an ABC: adapters
implement it through composition (they hold the real model/session as a
private attribute) instead of inheriting from a shared parent class.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np
from pydantic import BaseModel, ConfigDict


class FeatureVector(BaseModel):
    """Output of feature engineering; input to model inference."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    values: list[float]

    def to_numpy(self) -> np.ndarray:
        return np.asarray(self.values, dtype=np.float32).reshape(1, -1)


class Prediction(BaseModel):
    """Internal, framework-independent prediction result. Raw ONNX/sklearn/
    MLflow outputs must be converted into this before entering the domain."""

    label: str
    confidence: float
    model_name: str
    model_version: str
    raw_scores: dict[str, float] = {}


@runtime_checkable
class ModelProvider(Protocol):
    """Serves a single registered, versioned model for inference.

    Training happens offline (see docs/ml-architecture.md); this port is
    inference-only and must never be used to train a model inside a request
    handler. Implementations satisfy this structurally (duck typing) -- they
    do not inherit from it. The actual model/session an implementation wraps
    (e.g. an onnxruntime `InferenceSession`) should be held as a private
    attribute, never exposed.
    """

    @property
    def model_name(self) -> str: ...

    @property
    def model_version(self) -> str: ...

    def predict(self, features: FeatureVector) -> Prediction: ...
