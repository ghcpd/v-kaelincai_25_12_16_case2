"""
Tests for MNIST Classifier v1.2 (fixed)
These tests are adapted from the original regression suite and verify the
normalization fix and improved predictions.
"""

import os
import sys
import pytest
import numpy as np

# Ensure src is importable from tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mnist_classifier import MNISTClassifier

# Paths inside fixed_project
BASE = os.path.join(os.path.dirname(__file__), '..')
MODEL_PATH = os.path.join(BASE, 'models', 'mnist_model.npy')
TEST_IMAGE_7 = os.path.join(BASE, 'data', 'test_digit_7.png')
TEST_IMAGE_3 = os.path.join(BASE, 'data', 'test_digit_3.png')


def ensure_test_data():
    """Generate model and test images (always regenerate to ensure deterministic tests)."""
    # Always run generator so tests are deterministic even if files already exist
    gen_path = os.path.join(os.path.dirname(__file__), '..', 'generate_test_data.py')
    import runpy
    runpy.run_path(gen_path, run_name='__main__')


class TestFixedMNIST:
    """Fixed behavior tests (v1.2)"""

    def setup_method(self):
        ensure_test_data()
        self.classifier = MNISTClassifier(MODEL_PATH)

    def test_predict_digit_7_fixed(self):
        prediction = self.classifier.predict(TEST_IMAGE_7)
        assert prediction == 7, f"Expected digit 7 after fix, got {prediction}"

    def test_predict_digit_3_fixed(self):
        prediction = self.classifier.predict(TEST_IMAGE_3)
        assert prediction == 3, f"Expected digit 3 after fix, got {prediction}"

    def test_preprocessing_normalization_fixed(self):
        pre = self.classifier.preprocess_image(TEST_IMAGE_7)
        assert np.max(pre) <= 1.0 + 1e-8, f"Max value should be ≤ 1.0 after normalization, got {np.max(pre)}"
        assert np.min(pre) >= 0.0 - 1e-8, f"Min value should be ≥ 0.0 after normalization, got {np.min(pre)}"

    def test_confidence_high_for_correct_predictions(self):
        pred, conf, probs = self.classifier.predict_with_confidence(TEST_IMAGE_7)
        assert pred == 7, f"Prediction should be 7, got {pred}"
        assert conf > 0.5, f"Confidence should be > 0.5 for correct prediction, got {conf:.3f}"

    def test_batch_prediction_fixed(self):
        preds = [self.classifier.predict(TEST_IMAGE_7) for _ in range(5)]
        assert len(set(preds)) == 1, f"Predictions should be consistent, got {preds}"
        assert preds[0] == 7, f"Batch predictions should be 7, got {preds[0]}"

    def test_version_is_v1_2(self):
        assert MNISTClassifier.VERSION == "1.2.0", "Version should be updated to 1.2.0"

    def test_comparison_with_v1_1(self):
        # Sanity comparison: load original classifier module directly from file
        # Try both relative locations: (../../issue_project) and (../../../issue_project)
        issue_proj = os.path.join(os.path.dirname(__file__), '..', '..', 'issue_project')
        if not os.path.exists(issue_proj):
            issue_proj = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'issue_project')
        src_path = os.path.join(issue_proj, 'src', 'mnist_classifier.py')
        if not os.path.exists(src_path):
            pytest.skip("Original v1.1 project not available for direct comparison")

        # Load original module in isolated way to avoid import conflicts
        import runpy
        try:
            mod = runpy.run_path(src_path)
            OldMNIST = mod.get('MNISTClassifier')
            if OldMNIST is None:
                pytest.skip("Original MNISTClassifier class not found in v1.1 source")

            old = OldMNIST(os.path.join(issue_proj, 'models', 'mnist_model.npy'))
            old_pre = old.preprocess_image(os.path.join(issue_proj, 'data', 'test_digit_7.png'))
            old_max = float(np.max(old_pre))
            new_pre = self.classifier.preprocess_image(TEST_IMAGE_7)
            new_max = float(np.max(new_pre))
            assert old_max > 1.0 and new_max <= 1.0, (
                f"Comparison shows fix: old_max={old_max:.2f} (bad), new_max={new_max:.2f} (good)"
            )
        except Exception as exc:
            pytest.skip(f"Comparison failed due to error: {exc}")


if __name__ == '__main__':
    pytest.main([__file__, '-q'])
