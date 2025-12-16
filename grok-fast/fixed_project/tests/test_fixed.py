"""
Fixed tests for MNIST Classifier v1.2

These tests verify that the normalization bug has been fixed.
All tests should PASS with the corrected implementation.
"""

import sys
import os
import pytest
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mnist_classifier import MNISTClassifier


# Test configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'mnist_model.npy')
TEST_IMAGE_7 = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_digit_7.png')
TEST_IMAGE_3 = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_digit_3.png')


class TestFixedDigitPrediction:
    """Test suite to verify the normalization fix works correctly."""

    def setup_method(self):
        """Setup classifier before each test."""
        self.classifier = MNISTClassifier(MODEL_PATH)

    def test_predict_digit_7_fixed(self):
        """
        FIXED TEST: Digit 7 prediction should work correctly.

        This test PASSES in v1.2 because pixel normalization is restored.
        The model expects inputs in [0, 1] range, which is now provided.

        Expected: 7
        """
        prediction = self.classifier.predict(TEST_IMAGE_7)

        assert prediction == 7, (
            f"Expected digit 7, but got {prediction}. "
            f"Fix verification: normalization restored in v1.2."
        )

    def test_predict_digit_3_fixed(self):
        """
        FIXED TEST: Digit 3 prediction should work correctly.

        This test PASSES in v1.2 because pixel normalization is restored.
        Verifies the fix works for different digits.

        Expected: 3
        """
        prediction = self.classifier.predict(TEST_IMAGE_3)

        assert prediction == 3, (
            f"Expected digit 3, but got {prediction}. "
            f"Fix verification: normalization restored in v1.2."
        )

    def test_preprocessing_normalization_fixed(self):
        """
        UNIT TEST: Verify preprocessed image is in correct [0, 1] range.

        This test PASSES in v1.2 because:
        - preprocess_image() now includes img = img / 255.0
        - Outputs are correctly normalized to [0, 1] range

        Expected: max value ≈ 1.0, min value ≈ 0.0
        """
        preprocessed = self.classifier.preprocess_image(TEST_IMAGE_7)

        max_value = np.max(preprocessed)
        min_value = np.min(preprocessed)

        assert max_value <= 1.0, (
            f"Preprocessed image max value should be ≤ 1.0, got {max_value}. "
            f"Fix: normalization step restored."
        )

        assert min_value >= 0.0, (
            f"Preprocessed image min value should be ≥ 0.0, got {min_value}"
        )

        # Additional check: values should be properly normalized
        assert max_value > 0.0, (
            f"Preprocessed image should have non-zero values, got max {max_value}"
        )

    def test_confidence_high_for_correct_predictions(self):
        """
        CONFIDENCE TEST: Correct predictions should have high confidence.

        This test PASSES in v1.2 because:
        - With proper normalization, model receives expected input scale
        - Predictions are accurate with appropriate confidence levels

        Expected: prediction=7, confidence > 0.5
        """
        prediction, confidence, probs = self.classifier.predict_with_confidence(TEST_IMAGE_7)

        assert prediction == 7, (
            f"Expected digit 7, got {prediction}. "
            f"Confidence={confidence:.2f}, Probs={[f'{p:.2f}' for p in probs]}"
        )

        assert confidence > 0.5, (
            f"Expected high confidence (>0.5) for correct prediction, got {confidence:.2f}. "
            f"Fix: normalization enables reliable confidence scores."
        )

    def test_batch_prediction_fixed(self):
        """
        INTEGRATION TEST: Multiple predictions should be consistent and correct.

        This test PASSES in v1.2 because with proper normalization,
        predictions are stable and accurate.

        Expected: All predictions return 7
        """
        predictions = []
        for _ in range(5):
            pred = self.classifier.predict(TEST_IMAGE_7)
            predictions.append(pred)

        # All predictions should be the same
        assert len(set(predictions)) == 1, (
            f"Predictions should be consistent, got {predictions}"
        )

        # Should predict 7
        assert predictions[0] == 7, (
            f"Expected all predictions to be 7, got {predictions[0]}"
        )


class TestVersionAndComparison:
    """Tests for version verification and comparison with v1.1."""

    def test_version_is_v1_2(self):
        """Verify this is the fixed v1.2.0."""
        assert MNISTClassifier.VERSION == "1.2.0", (
            f"Expected version 1.2.0, got {MNISTClassifier.VERSION}. "
            "This should be the fixed version."
        )

    def test_comparison_with_v1_1(self):
        """
        COMPARISON TEST: Demonstrate the fix effect.

        This test shows the difference between v1.1 (buggy) and v1.2 (fixed).
        In v1.1, preprocessing would output values in [0, 255] range.
        In v1.2, preprocessing correctly outputs values in [0, 1] range.

        Expected: Preprocessed values in [0, 1] range
        """
        classifier = MNISTClassifier(MODEL_PATH)

        # Get preprocessed data
        preprocessed = classifier.preprocess_image(TEST_IMAGE_7)

        # Verify normalization
        max_val = np.max(preprocessed)
        min_val = np.min(preprocessed)

        # Should be in [0, 1] range (fixed in v1.2)
        assert 0.0 <= min_val <= 1.0, f"Min value {min_val} should be in [0, 1]"
        assert 0.0 <= max_val <= 1.0, f"Max value {max_val} should be in [0, 1]"

        # Test prediction accuracy
        prediction = classifier.predict(TEST_IMAGE_7)
        assert prediction == 7, f"Should correctly predict 7, got {prediction}"

        # This demonstrates the fix: v1.1 would have max_val ≈ 255, prediction wrong


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])