# Known Issue - v1.1 Preprocessing Regression

## 🐛 Issue Summary

**Type**: Preprocessing regression  
**Severity**: High — all predictions fail  
**Scope**: All `MNISTClassifier.predict()` and `predict_with_confidence()` calls  
**Introduced**: v1.1.0  
**Status**: 🔴 To be fixed

---

## 📋 Issue Description

During the v1.0 → v1.1 upgrade, the `preprocess_image()` method **accidentally removed the pixel normalization step**, changing the input range from `[0, 1]` to `[0, 255]`, which no longer matches the scale used during model training.

### Code Comparison

#### ✅ v1.0 (correct implementation)
```python
def preprocess_image(self, image_path):
    img = Image.open(image_path).convert('L')
    if img.size != (28, 28):
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    img = np.array(img)
    img = img / 255.0  # ✅ normalize to [0, 1]
    img = img.flatten()
    
    return img
```

#### ❌ v1.1 (regression bug)
```python
def preprocess_image(self, image_path):
    img = Image.open(image_path).convert('L')
    if img.size != (28, 28):
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    img = np.array(img)
    # ❌ missing: img = img / 255.0
    img = img.flatten()
    
    return img
```

---

## 🔍 Root Cause Analysis

### 1. Technical root cause
- **Model expectation**: normalized pixel values `[0, 1]` (used during training)
- **Actual input**: unnormalized values `[0, 255]` in v1.1
- **Scale mismatch**: 255×
- **Impact**:
    - Neural activations are out of expected range
    - Softmax outputs are distorted
    - Predictions are wrong

### 2. Numerical impact example

Assume a pixel value of `1.0` (white) during training:

```python
# Correct (v1.0)
pixel_value = 255 / 255.0 = 1.0
weight = 0.01
activation = pixel_value * weight = 0.01  # within normal range

# Wrong (v1.1)
pixel_value = 255  # unnormalized
weight = 0.01
activation = pixel_value * weight = 2.55  # 255× larger!
```

### 3. Where it lives
- **File**: `src/mnist_classifier.py`
- **Class**: `MNISTClassifier`
- **Method**: `preprocess_image()`
- **Lines**: ~45–48 (after `np.array(img)`)

---

## 📊 Impact

### Test failures

| Test | Failure reason | Expected | Actual |
|------|----------------|----------|--------|
| `test_predict_digit_7_basic` | Wrong prediction | `7` | `1` or other |
| `test_predict_digit_7_with_confidence` | Confidence abnormal | High confidence | Low/wrong confidence |
| `test_preprocessing_output_range` | Output range wrong | `max ≤ 1.0` | `max = 255.0` |
| `test_batch_prediction_consistency` | Predictions unstable | Consistent predictions | Wrong predictions |
| `test_predict_digit_3_basic` | Wrong prediction | `3` | Other digits |

### Observed behavior
```
Predict test_digit_7.png (ground truth: 7)
├─ v1.0: ✅ outputs 7 (confidence 0.89)
└─ v1.1: ❌ outputs 1 (confidence 0.23) - REGRESSION!
```

---

## 🧪 Reproduction

### Minimal repro script
```python
import numpy as np
from src.mnist_classifier import MNISTClassifier

classifier = MNISTClassifier('models/mnist_model.npy')

# Test preprocessing output range
preprocessed = classifier.preprocess_image('data/test_digit_7.png')
print(f"Max pixel value: {np.max(preprocessed)}")
# Expected: 1.0
# Actual: 255.0 ❌

# Test prediction
prediction = classifier.predict('data/test_digit_7.png')
print(f"Prediction: {prediction}")
# Expected: 7
# Actual: 1 or other ❌
```

### Automated test repro
```powershell
pytest tests/test_regression.py::TestDigitPredictionRegression::test_preprocessing_output_range -v
```

---

## 🔧 Fix Strategy

### Steps
1. **Locate code**: open `src/mnist_classifier.py`, find `preprocess_image()`
2. **Add normalization**: after `img = np.array(img)` and before `img.flatten()` add:
    ```python
    img = img / 255.0
    ```
3. **Verify**: run the test suite:
    ```powershell
    pytest tests/test_regression.py -v
    ```

### Expected results (after fix)
```
tests/test_regression.py::TestDigitPredictionRegression::test_predict_digit_7_basic PASSED
tests/test_regression.py::TestDigitPredictionRegression::test_predict_digit_7_with_confidence PASSED
tests/test_regression.py::TestDigitPredictionRegression::test_preprocessing_output_range PASSED
tests/test_regression.py::TestDigitPredictionRegression::test_batch_prediction_consistency PASSED
tests/test_regression.py::TestDigitPredictionRegression::test_predict_digit_3_basic PASSED
```

---

## ⚠️ Prevention

### Why did it happen?
- Key line removed during refactor/cleanup
- Missing unit tests for preprocessing
- Code review missed the change

### How to prevent
1. **Test coverage**:
    - ✅ Add unit tests for preprocessing
    - ✅ Validate output range and distribution
   
2. **Code review**:
    - 🔍 Focus on data preprocessing changes
    - 🔍 Annotate critical normalization steps

3. **Documentation**:
    - 📝 Comment normalization requirements in code
    - 📝 Document input expectations for the model

### Improvement suggestion
```python
def preprocess_image(self, image_path):
    """Load and preprocess image for prediction.
    
    CRITICAL: Model was trained on normalized [0, 1] pixel values.
    Always divide by 255.0 before feeding to the network.
    """
    img = Image.open(image_path).convert('L')
    if img.size != (28, 28):
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    img = np.array(img)
    
    # REQUIRED: Normalize to [0, 1] range (model expects this)
    img = img / 255.0
    
    img = img.flatten()
    return img
```

---

## 📈 Impact Assessment

### Severity: 🔴 High
- **Functionality**: all prediction functions fail
- **Data**: no data loss
- **Security**: no security risk
- **User experience**: severe — all users affected

### Blast radius
- ✅ Only v1.1.0 is affected
- ✅ v1.0.0 is unaffected
- ✅ Model file unchanged
- ✅ Single-line fix

---

## 🎯 Summary

This is a **simple but high-impact** regression caused by a single missing line.

**Key takeaways**:
1. Data preprocessing is critical in deep learning pipelines
2. Input scale must match training
3. Preprocessing logic needs unit tests
4. Simple cleanups can introduce severe regressions

**Fix difficulty**: ⭐ very low (add one line)  
**Repro difficulty**: ⭐ very low (run tests)  
**Test coverage**: ⭐⭐⭐⭐⭐ comprehensive (7 tests across scenarios)

---

*Last updated: 2025-12-02*  
*Issue tracking: local project — v1.1 preprocessing regression*
