"""ONNX Runtime adapter. Translates onnxruntime's raw ndarray outputs into
the internal `Prediction` type. This is the only file in the codebase allowed
to import onnxruntime.

Implements the `ModelProvider` port structurally (Protocol / duck typing),
via composition rather than inheritance: the onnxruntime `InferenceSession`
is wrapped as a private attribute (`__session`) and never exposed outside
this class.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import onnxruntime as ort

from aiseo.domain.errors import InvalidModelOutputError
from aiseo.infrastructure.observability.logging import get_logger
from aiseo.ports.ml.model_provider import FeatureVector, Prediction

logger = get_logger(__name__)


class OnnxModelProvider:
    """Loads a single ONNX model and serves inference.

    Model lifecycle (loading, caching) is owned by whoever constructs this
    adapter (typically the composition root or a cached factory) -- this
    class does not manage global mutable state itself. The wrapped ONNX
    session is a private implementation detail (composition), not inherited
    behavior.
    """

    def __init__(
        self,
        model_path: Path,
        model_name: str,
        model_version: str,
        class_labels: list[str],
        providers: list[str] | None = None,
    ) -> None:
        if not model_path.exists():
            raise FileNotFoundError(f"ONNX model not found at {model_path}")
        self.__model_name = model_name
        self.__model_version = model_version
        self.__class_labels = class_labels
        self.__session = ort.InferenceSession(
            str(model_path),
            providers=providers or ["CPUExecutionProvider"],
        )
        self.__input_name = self.__session.get_inputs()[0].name
        logger.info(
            "onnx_model.loaded",
            model_name=model_name,
            model_version=model_version,
            input_name=self.__input_name,
        )

    @property
    def model_name(self) -> str:
        return self.__model_name

    @property
    def model_version(self) -> str:
        return self.__model_version

    def predict(self, features: FeatureVector) -> Prediction:
        inputs = {self.__input_name: features.to_numpy()}
        outputs = self.__session.run(None, inputs)
        scores = np.asarray(outputs[0]).reshape(-1)

        if scores.shape[0] != len(self.__class_labels):
            logger.error(
                "onnx_model.output_shape_mismatch",
                model_name=self.__model_name,
                model_version=self.__model_version,
                returned=scores.shape[0],
                expected=len(self.__class_labels),
            )
            raise InvalidModelOutputError(
                f"Model {self.__model_name}:{self.__model_version} returned "
                f"{scores.shape[0]} scores but {len(self.__class_labels)} labels are configured"
            )

        best_index = int(np.argmax(scores))
        raw_scores = {
            label: float(score) for label, score in zip(self.__class_labels, scores, strict=True)
        }

        return Prediction(
            label=self.__class_labels[best_index],
            confidence=float(scores[best_index]),
            model_name=self.__model_name,
            model_version=self.__model_version,
            raw_scores=raw_scores,
        )
