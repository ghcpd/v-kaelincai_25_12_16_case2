# MNIST Classifier - Regression Bug Project

## 🎯 Project Overview

This MNIST handwritten digit classification project **deliberately injects a simple regression** to demonstrate how a preprocessing bug can break a model.

**Scenario**: When upgrading the MNIST classification script from v1.0 to v1.1, the pixel normalization step (`img = img / 255.0`) was accidentally removed, causing predictions that previously worked to fail.

---

## 📁 Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   └── mnist_classifier.py        # Core classifier (v1.1 contains the regression bug)
├── tests/
│   ├── __init__.py
│   └── test_regression.py         # Regression tests (expected to fail due to the bug)
├── models/
│   └── mnist_model.npy            # Pretrained model weights (expects normalized input)
├── data/
│   ├── test_digit_7.png           # Test image: digit 7
│   └── test_digit_3.png           # Test image: digit 3
├── generate_test_data.py          # Script to generate test data
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── README.md                      # This file
└── KNOWN_ISSUE.md                 # Detailed issue explanation
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.8+
- Windows 11
- PowerShell

### One-click run

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate test data (model and test images)
python generate_test_data.py

# 3. Run tests (you will see failures)
pytest tests/test_regression.py -v
```

---

## 🐛 Bug Details

### Bug type
**Preprocessing regression** — missing normalization.

### Trigger conditions
- Use `MNISTClassifier` v1.1
- Call `predict()` or `predict_with_confidence()` on any test image

### Expected vs. actual

| Scenario | v1.0 (Expected) | v1.1 (Actual) |
|----------|-----------------|---------------|
| Predict `test_digit_7.png` | ✅ Outputs `7` | ❌ Outputs `1` or another wrong digit |
| Preprocessing output range | ✅ `[0.0, 1.0]` | ❌ `[0, 255]` |
| Prediction confidence | ✅ High (>0.5) | ❌ Low or wrong |

### Root cause analysis
- **File**: `src/mnist_classifier.py`
- **Function**: `MNISTClassifier.preprocess_image()`
- **Lines**: ~45–48
- **Core issue**:
  ```python
  # v1.0 (correct)
  img = np.array(img)
  img = img / 255.0  # normalize to [0, 1]
  img = img.flatten()
  
  # v1.1 (bug)
  img = np.array(img)
  # missing normalization!
  img = img.flatten()
  ```

---

## 🧪 Tests

The project includes **7 automated tests**. With the current bug, **5 are expected to fail** and **2 pass (sanity checks)**.

### Test status
1. ❌ `test_predict_digit_7_basic` — basic digit 7 prediction
2. ❌ `test_predict_digit_7_with_confidence` — confidence check
3. ❌ `test_preprocessing_output_range` — preprocessing range unit test
4. ❌ `test_batch_prediction_consistency` — batch prediction consistency
5. ❌ `test_predict_digit_3_basic` — digit 3 prediction
6. ✅ `test_model_loads_successfully` — model loads successfully
7. ✅ `test_version_is_v1_1` — version verification

### Run tests

```powershell
# Run all tests
pytest tests/test_regression.py -v

# Run a single test
pytest tests/test_regression.py::TestDigitPredictionRegression::test_predict_digit_7_basic -v

# Show full tracebacks
pytest tests/test_regression.py -v --tb=long
```

---

## 📊 Reproduction Steps

### Option 1: via tests
```powershell
pytest tests/test_regression.py -v
```

### Option 2: manual CLI
```powershell
# Predict digit 7 (should return 7 but returns a wrong digit)
python src/mnist_classifier.py models/mnist_model.npy data/test_digit_7.png
```

### Option 3: Python script
```python
from src.mnist_classifier import MNISTClassifier

classifier = MNISTClassifier('models/mnist_model.npy')
prediction = classifier.predict('data/test_digit_7.png')
print(f"Predicted: {prediction}")  # Expected: 7, Actual (v1.1): 1 or other
```

---

## 🔧 Fix Hints

**Do not provide the full fix in this exercise**, but you can resolve the issue by:

1. Inspecting `preprocess_image()`
2. Comparing v1.0 vs. v1.1
3. Ensuring pixel values are normalized to `[0, 1]`
4. Re-running the tests to verify

See `KNOWN_ISSUE.md` for the detailed analysis.

---

## 📚 Tech Stack

- **Language**: Python 3.8+
- **Dependencies**:
  - `numpy==1.24.3` — numerical computing
  - `Pillow==10.0.0` — image processing
  - `pytest==7.4.0` — testing
- **Platform**: Windows 11

---

## 🎓 Learning Value

This project demonstrates:
- ✅ The impact of preprocessing regressions
- ✅ How to catch regressions with unit tests
- ✅ Why input scaling matters for deep learning
- ✅ A test-driven bug-fix workflow

---

## 📝 Version History

- **v1.1.0** (current) — ⚠️ Regression: removed pixel normalization
- **v1.0.0** — ✅ Initial version, predictions correct

---

## 📞 Troubleshooting

If you hit issues:

1. **Missing test data**: run `python generate_test_data.py`
2. **Import errors**: run commands from the project root
3. **Dependency issues**: `pip install -r requirements.txt --upgrade`

---

## 📖 Further Reading

- `KNOWN_ISSUE.md` — detailed analysis and fix hints
- `tests/test_regression.py` — full test suite
- `src/mnist_classifier.py` — source code with bug annotations
