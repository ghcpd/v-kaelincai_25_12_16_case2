"""
Test suite for MNIST Classifier v1.2 (fixed version)
"""
import os
import sys
import subprocess
import numpy as np

# Ensure local src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mnist_classifier import MNISTClassifier

# Paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_PATH = os.path.join(ROOT, 'models', 'mnist_model.npy')
TEST_IMAGE_7 = os.path.join(ROOT, 'data', 'test_digit_7.png')
TEST_IMAGE_3 = os.path.join(ROOT, 'data', 'test_digit_3.png')


def setup_module(module):
    """Generate or copy test data and model if missing."""
    script = os.path.join(ROOT, 'generate_test_data.py')
    if not os.path.exists(MODEL_PATH) or not os.path.exists(TEST_IMAGE_7):
        subprocess.check_call([sys.executable, script])


class TestFixedClassifier:
    def setup_method(self):
        self.classifier = MNISTClassifier(MODEL_PATH)

    def test_predict_digit_7_fixed(self):
        pred = self.classifier.predict(TEST_IMAGE_7)
        assert pred == 7, f"Expected 7, got {pred}"

    def test_predict_digit_3_fixed(self):
        pred = self.classifier.predict(TEST_IMAGE_3)
        assert pred == 3, f"Expected 3, got {pred}"

    def test_preprocessing_normalization_fixed(self):
        pre = self.classifier.preprocess_image(TEST_IMAGE_7)
        assert np.max(pre) <= 1.0 and np.min(pre) >= 0.0, (
            f"Preprocessing should normalize to [0,1], got min={np.min(pre)}, max={np.max(pre)}"
        )

    def test_confidence_high_for_correct_predictions(self):
        pred, conf, probs = self.classifier.predict_with_confidence(TEST_IMAGE_7)
        assert pred == 7, f"Expected 7, got {pred}"
        assert conf > 0.5, f"Expected confidence >0.5, got {conf:.2f}"

    def test_batch_prediction_fixed(self):
        preds = [self.classifier.predict(TEST_IMAGE_7) for _ in range(5)]
        assert len(set(preds)) == 1 and preds[0] == 7, f"Batch predictions inconsistent: {preds}"

    def test_version_is_v1_2(self):
        assert MNISTClassifier.VERSION == "1.2.0", "Version should be 1.2.0"

    def test_comparison_with_v1_1(self):
        # Import v1.1 classifier from issue_project to compare behavior
        issue_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'issue_project', 'src'))
        sys.path.insert(0, issue_src)
        from mnist_classifier import MNISTClassifier as OldClassifier

        # Use original unmodified model for comparison (issue_project) to show improvement
        # Path to original (unmodified) model in workspace root issue_project
        # Use absolute path to original model in workspace root (issue_project)
        original_model = r'c:\\BugBash\\workSpace1\\issue_project\\models\\mnist_model.npy'
        assert os.path.exists(original_model), f"Original model not found at {original_model}"
        old = OldClassifier(original_model)
        new = self.classifier

        old_pred, old_conf, _ = old.predict_with_confidence(TEST_IMAGE_7)
        new_pred, new_conf, _ = new.predict_with_confidence(TEST_IMAGE_7)

        assert new_pred == 7 and new_conf > 0.5, (
            f"Fixed classifier should predict 7 with high confidence, got pred={new_pred}, conf={new_conf}"
        )

        # The old classifier should either be wrong or have lower confidence
        assert old_pred != 7 or old_conf < new_conf, (
            "Old classifier (v1.1) should perform worse or have lower confidence than fixed v1.2"
        )
