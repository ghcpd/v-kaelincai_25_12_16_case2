# Project Structure Overview

```
issue_project/
│
├── README.md                      # Main doc (quickstart, usage)
├── KNOWN_ISSUE.md                 # Detailed issue analysis & fix guide
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── .gitignore                     # Git ignore rules
│
├── run_demo.bat                   # Windows batch launcher
├── run_demo.ps1                   # PowerShell launcher
├── generate_test_data.py          # Generates model & test images
│
├── src/                           # Source code
│   ├── __init__.py
│   └── mnist_classifier.py        # ⚠️ Core classifier (regression bug)
│
├── tests/                         # Tests
│   ├── __init__.py
│   └── test_regression.py         # Regression suite (7 tests)
│
├── models/                        # Model files (generated)
│   └── mnist_model.npy            # Mock weights
│
└── data/                          # Test data (generated)
  ├── test_digit_7.png           # Test image: digit 7
  └── test_digit_3.png           # Test image: digit 3
```

## 📂 Key Files

### Source

- **`src/mnist_classifier.py`**  
  MNIST classifier. v1.1 deliberately removes pixel normalization (lines ~45–48), causing prediction failures.

### Tests

- **`tests/test_regression.py`**  
  7 test cases:
  - 5 failing tests (expose the regression)
  - 2 passing tests (model loading & version check)

### Config

- **`requirements.txt`**: `numpy`, `Pillow`, `pytest`
- **`pytest.ini`**: Pytest configuration (paths and naming)

### Docs

- **`README.md`**: Quickstart, structure, run guide
- **`KNOWN_ISSUE.md`**: Detailed analysis, root cause, fix hints

### Tooling

- **`generate_test_data.py`**: Generates mock model and test images
- **`run_demo.bat`** / **`run_demo.ps1`**: One-click demo scripts

## 🔍 Bug Location

**File**: `src/mnist_classifier.py`  
**Method**: `MNISTClassifier.preprocess_image()`  
**Lines**: ~45–48

```python
# Current (v1.1, buggy)
img = np.array(img)
# Missing: img = img / 255.0  ← BUG!
img = img.flatten()
```

## 🧪 Test Failures

Run `pytest tests/test_regression.py -v`:

```
FAILED test_predict_digit_7_with_confidence    # Confidence too low (0.32 < 0.5)
FAILED test_preprocessing_output_range         # Range wrong (255 vs 1.0)
FAILED test_predict_digit_3_basic              # Wrong prediction (0 vs 3)
PASSED test_predict_digit_7_basic              # Passes by coincidence (model bias)
PASSED test_batch_prediction_consistency       # Consistency passes
PASSED test_model_loads_successfully           # Model loads
PASSED test_version_is_v1_1                    # Version check
```

## 📊 File Sizes

- Source: ~4 KB
- Tests: ~6 KB
- Docs: ~15 KB (README + KNOWN_ISSUE)
- Model: ~330 KB (.npy)
- Images: ~1 KB × 2

**Total**: ~360 KB (including generated files)

## 🎯 Highlights

✅ **Minimal**: only core functionality, no extra deps  
✅ **Runnable**: single command to test  
✅ **Clear**: bug is explicitly marked  
✅ **Tested**: 7 tests across scenarios  
✅ **Documented**: README + KNOWN_ISSUE

## 💡 Next Steps

1. **Understand**: read `KNOWN_ISSUE.md`
2. **Inspect**: check `src/mnist_classifier.py` lines ~45–48
3. **Run tests**: `pytest tests/test_regression.py -v`
4. **Fix**: add normalization
5. **Verify**: re-run tests, ensure all pass
