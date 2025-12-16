"""
Fixed project tests for MNISTClassifier v1.2 (fixed bug) and comparison to v1.1
"""

import sys
import os
import pytest
import numpy as np

# Add fixed_project src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mnist_classifier import MNISTClassifier

# Test configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'mnist_model.npy')
TEST_IMAGE_7 = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_digit_7.png')
TEST_IMAGE_3 = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_digit_3.png')


class TestMNISTClassifierFixed:
    """Tests verifying the fixed behavior (v1.2)"""

    def setup_method(self):
        self.classifier = MNISTClassifier(MODEL_PATH)

    def test_predict_digit_7_fixed(self):
        prediction = self.classifier.predict(TEST_IMAGE_7)
        assert prediction == 7, f"Expected digit 7, got {prediction}"

    def test_predict_digit_3_fixed(self):
        prediction = self.classifier.predict(TEST_IMAGE_3)
        assert prediction == 3, f"Expected digit 3, got {prediction}"

    def test_preprocessing_normalization_fixed(self):
        preprocessed = self.classifier.preprocess_image(TEST_IMAGE_7)
        assert np.max(preprocessed) <= 1.0 + 1e-6
        assert np.min(preprocessed) >= 0.0 - 1e-6

    def test_confidence_high_for_correct_predictions(self):
        pred, confidence, probs = self.classifier.predict_with_confidence(TEST_IMAGE_7)
        assert pred == 7
        assert confidence > 0.5, f"Confidence should be >0.5 for correct prediction (got {confidence})"

    def test_batch_prediction_fixed(self):
        preds = [self.classifier.predict(TEST_IMAGE_7) for _ in range(5)]
        assert len(set(preds)) == 1
        assert preds[0] == 7

    def test_version_is_v1_2(self):
        assert MNISTClassifier.VERSION == "1.2.0"


class TestComparisonWithV1_1:
    """Comparison test showing the effect of the fix vs the buggy v1.1 implementation"""

    def setup_method(self):
        # Fixed classifier should use the fixed_project model (normalization present)
        fixed_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'mnist_model.npy'))
        self.fixed = MNISTClassifier(fixed_model_path)

        # Dynamically load the v1.1 classifier from issue_project
        from importlib import util
        old_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'issue_project', 'src', 'mnist_classifier.py'))
        spec = util.spec_from_file_location('mnist_classifier_v1_1', old_src_path)
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Use the original issue_project model and images for the v1.1 classifier
        issue_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'issue_project', 'models', 'mnist_model.npy'))
        self.old_classifier = mod.MNISTClassifier(issue_model_path)

        # Store issue_project image paths for use in comparison tests
        self.issue_image_7 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'issue_project', 'data', 'test_digit_7.png'))
        self.issue_image_3 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'issue_project', 'data', 'test_digit_3.png'))

    def test_comparison_with_v1_1(self):
        # Fixed version should predict correctly for both images
        fixed_pred_7 = self.fixed.predict(TEST_IMAGE_7)
        fixed_pred_3 = self.fixed.predict(TEST_IMAGE_3)
        assert fixed_pred_7 == 7
        assert fixed_pred_3 == 3

        # v1.1 buggy version should differ from the fixed version on at least one image
        old_pred_7 = self.old_classifier.predict(TEST_IMAGE_7)
        old_pred_3 = self.old_classifier.predict(TEST_IMAGE_3)

        # Ensure predictions differ between versions (showing the fix effect)
        assert (old_pred_7 != fixed_pred_7) or (old_pred_3 != fixed_pred_3), (
            f"Old v1.1 and fixed versions should predict differently; old: 7={old_pred_7}, 3={old_pred_3}, fixed: 7={fixed_pred_7}, 3={fixed_pred_3}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
