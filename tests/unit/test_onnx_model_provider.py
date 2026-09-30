from pathlib import Path

import pytest

from aiseo.adapters.ml.onnx_model_provider import OnnxModelProvider
from aiseo.ports.ml.model_provider import FeatureVector

MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "intent_classifier_v1.onnx"


@pytest.fixture()
def provider() -> OnnxModelProvider:
    return OnnxModelProvider(
        model_path=MODEL_PATH,
        model_name="intent-classifier",
        model_version="v1",
        class_labels=["INFORMATIONAL", "COMMERCIAL", "TRANSACTIONAL"],
    )


def test_predict_returns_internal_prediction_type(provider: OnnxModelProvider) -> None:
    features = FeatureVector(values=[1.0, 0.5, 0.2, 0.1])

    prediction = provider.predict(features)

    assert prediction.model_name == "intent-classifier"
    assert prediction.model_version == "v1"
    assert prediction.label in {"INFORMATIONAL", "COMMERCIAL", "TRANSACTIONAL"}
    assert set(prediction.raw_scores) == {"INFORMATIONAL", "COMMERCIAL", "TRANSACTIONAL"}
    assert prediction.confidence == max(prediction.raw_scores.values())


def test_missing_model_file_raises() -> None:
    with pytest.raises(FileNotFoundError):
        OnnxModelProvider(
            model_path=Path("/nonexistent/model.onnx"),
            model_name="x",
            model_version="v1",
            class_labels=["A"],
        )
