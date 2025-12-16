"""
Regression tests for MNIST Classifier v1.1

These tests expose the normalization bug introduced in v1.1.
All tests should FAIL with current implementation.
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


class TestDigitPredictionRegression:
    """Test suite to expose the normalization regression bug."""
    
    def setup_method(self):
        """Setup classifier before each test."""
        self.classifier = MNISTClassifier(MODEL_PATH)
    
    def test_predict_digit_7_basic(self):
        """
        REGRESSION TEST: Digit 7 prediction should work (as in v1.0).
        
        This test FAILS in v1.1 due to missing pixel normalization.
        In v1.0, this test passed because images were normalized to [0, 1].
        In v1.1, raw pixel values [0, 255] are used, causing wrong predictions.
        
        Expected: 7
        Actual (v1.1): Random incorrect digit (often 1 or other)
        """
        prediction = self.classifier.predict(TEST_IMAGE_7)
        
        assert prediction == 7, (
            f"Regression detected! Expected digit 7, but got {prediction}. "
            f"This worked in v1.0 but fails in v1.1 due to missing normalization."
        )
    
    def test_predict_digit_7_with_confidence(self):
        """
        REGRESSION TEST: Digit 7 should have high confidence.
        
        This test FAILS because:
        - Without normalization, input scale is 255x larger than expected
        - Model weights are trained for [0, 1] range
        - Prediction confidence is unreliable with wrong input scale
        
        Expected: prediction=7, confidence > 0.5
        Actual (v1.1): Wrong prediction with low/high confidence
        """
        prediction, confidence, probs = self.classifier.predict_with_confidence(TEST_IMAGE_7)
        
        assert prediction == 7, (
            f"Expected digit 7, got {prediction}. "
            f"Confidence={confidence:.2f}, Probs={[f'{p:.2f}' for p in probs]}"
        )
        
        assert confidence > 0.5, (
            f"Expected high confidence (>0.5) for digit 7, got {confidence:.2f}. "
            f"Low confidence indicates preprocessing issue."
        )
    
    def test_preprocessing_output_range(self):
        """
        UNIT TEST: Verify preprocessed image is in correct range.
        
        This test FAILS because:
        - preprocess_image() should output values in [0, 1] range
        - Due to missing normalization, outputs are in [0, 255] range
        
        Expected: max value ≈ 1.0
        Actual (v1.1): max value = 255.0
        """
        preprocessed = self.classifier.preprocess_image(TEST_IMAGE_7)
        
        max_value = np.max(preprocessed)
        min_value = np.min(preprocessed)
        
        assert max_value <= 1.0, (
            f"Preprocessed image max value should be ≤ 1.0, got {max_value}. "
            f"Missing normalization: pixel values should be divided by 255.0"
        )
        
        assert min_value >= 0.0, (
            f"Preprocessed image min value should be ≥ 0.0, got {min_value}"
        )
    
    def test_batch_prediction_consistency(self):
        """
        INTEGRATION TEST: Multiple predictions should be consistent.
        
        This test FAILS because without proper normalization,
        predictions are unstable and incorrect.
        
        Expected: All predictions return 7
        Actual (v1.1): Inconsistent or all wrong
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
    
    def test_predict_digit_3_basic(self):
        """
        REGRESSION TEST: Digit 3 prediction should work.
        
        Another test case to verify the normalization bug affects
        all predictions, not just digit 7.
        
        Expected: 3
        Actual (v1.1): Random incorrect digit
        """
        prediction = self.classifier.predict(TEST_IMAGE_3)
        
        assert prediction == 3, (
            f"Expected digit 3, but got {prediction}. "
            f"Normalization bug affects all digit predictions."
        )


class TestModelIntegrity:
    """Additional tests to verify model loading and structure."""
    
    def test_model_loads_successfully(self):
        """Sanity check: Model should load without errors."""
        classifier = MNISTClassifier(MODEL_PATH)
        
        assert classifier.weights is not None
        assert classifier.w1.shape == (784, 128)
        assert classifier.w2.shape == (128, 10)
        assert classifier.b1.shape == (128,)
        assert classifier.b2.shape == (10,)
    
    def test_version_is_v1_1(self):
        """Verify this is v1.1 with the regression bug."""
        assert MNISTClassifier.VERSION == "1.1.0", (
            "These tests are designed for v1.1.0 with the normalization bug"
        )


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
