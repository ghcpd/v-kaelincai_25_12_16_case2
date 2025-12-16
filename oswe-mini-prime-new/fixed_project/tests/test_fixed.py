"""Test suite for MNIST Classifier v1.2 (fixed)."""
import os
import sys
import runpy
from pathlib import Path
import numpy as np

# Project root for fixed project
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'

# Ensure src on path
sys.path.insert(0, str(SRC))
from mnist_classifier import MNISTClassifier

# Paths
MODEL_PATH = str(ROOT / 'models' / 'mnist_model.npy')
TEST_IMAGE_7 = str(ROOT / 'data' / 'test_digit_7.png')
TEST_IMAGE_3 = str(ROOT / 'data' / 'test_digit_3.png')


def ensure_test_data():
    """Generate model and images if they don't exist."""
    if not (Path(MODEL_PATH).exists() and Path(TEST_IMAGE_7).exists() and Path(TEST_IMAGE_3).exists()):
        # Run the generate_test_data.py script
        script_path = str(ROOT / 'generate_test_data.py')
        runpy.run_path(script_path, run_name='__main__')


class TestFixedClassifier:
    def setup_method(self):
        ensure_test_data()
        self.classifier = MNISTClassifier(MODEL_PATH)

    def test_predict_digit_7_fixed(self):
        prediction = self.classifier.predict(TEST_IMAGE_7)
        assert prediction == 7, f"Expected digit 7 but got {prediction}"

    def test_predict_digit_3_fixed(self):
        prediction = self.classifier.predict(TEST_IMAGE_3)
        assert prediction == 3, f"Expected digit 3 but got {prediction}"

    def test_preprocessing_normalization_fixed(self):
        pre = self.classifier.preprocess_image(TEST_IMAGE_7)
        assert np.max(pre) <= 1.0, f"Max preprocessed value should be <=1.0, got {np.max(pre)}"
        assert np.min(pre) >= 0.0, f"Min preprocessed value should be >=0.0, got {np.min(pre)}"

    def test_confidence_high_for_correct_predictions(self):
        pred, conf, probs = self.classifier.predict_with_confidence(TEST_IMAGE_7)
        assert pred == 7, f"Expected 7, got {pred}"
        assert conf > 0.5, f"Expected high confidence >0.5, got {conf}"

    def test_batch_prediction_fixed(self):
        preds = [self.classifier.predict(TEST_IMAGE_7) for _ in range(5)]
        assert len(set(preds)) == 1, f"Predictions should be consistent, got {preds}"
        assert preds[0] == 7, f"Expected predictions to be 7, got {preds[0]}"

    def test_version_is_v1_2(self):
        assert MNISTClassifier.VERSION == "1.2.0", "Version should be 1.2.0"

    def test_comparison_with_v1_1(self):
        # Import v1.1 classifier from issue_project (load module directly to avoid import caching)
        issue_src = Path(__file__).resolve().parents[3] / 'issue_project' / 'src' / 'mnist_classifier.py'
        import importlib.util
        spec = importlib.util.spec_from_file_location('mnist_v1', str(issue_src))
        mnist_v1 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mnist_v1)
        MNISTV1 = mnist_v1.MNISTClassifier

        v1 = MNISTV1(MODEL_PATH)
        v2 = self.classifier

        pre_v1 = v1.preprocess_image(TEST_IMAGE_7)
        pre_v2 = v2.preprocess_image(TEST_IMAGE_7)

        assert np.max(pre_v1) > 1.0, "v1.1 preprocessing should be unnormalized (>1.0)"
        assert np.max(pre_v2) <= 1.0, "v1.2 preprocessing should be normalized (<=1.0)"


if __name__ == '__main__':
    import pytest
    pytest.main(['-q', __file__])
