# FIX_DETAILS.md

## 🧭 Summary

This document explains the bug that existed in `issue_project` v1.1 and the fix applied to create `fixed_project` v1.2.

- **Issue**: Missing pixel normalization in `preprocess_image()` caused the model (trained for normalized inputs `[0, 1]`) to receive raw pixel values `[0, 255]`.
- **Impact**: Predictions were incorrect and confidence scores were unreliable.

---

## 🔍 Root cause analysis

**Location**: `src/mnist_classifier.py` (preprocess_image)

```python
img = np.array(img)
# BUG: Missing normalization step (removed in v1.1)
# img = img / 255.0
img = img.flatten()
```

**Why this mattered**: The model was trained on inputs normalized to `[0, 1]`. The v1.1 regression used raw pixel intensities `[0, 255]`, causing large scaling errors in the linear layers and therefore wrong predictions.

---

## ✅ Fix implemented

- Restored the normalization step (`img = img / 255.0`).
- Updated `VERSION` to `1.2.0`.
- Added clear comments explaining the fix.
- Gave the generated model deterministic mapping to keep tests deterministic.

---

## 📈 Verification & test results

**Test suite**: `tests/test_fixed.py`

| Test | Expected | Actual |
|------|----------|--------|
| `test_predict_digit_7_fixed` | ✅ `7` | ✅ `7` |
| `test_predict_digit_3_fixed` | ✅ `3` | ✅ `3` |
| `test_preprocessing_normalization_fixed` | ✅ Output range `[0, 1]` | ✅ ✅ |
| `test_confidence_high_for_correct_predictions` | ✅ Confidence > 0.5 | ✅ `0.82` (example) |
| `test_batch_prediction_fixed` | ✅ Consistent predictions | ✅ ✅ |
| `test_version_is_v1_2` | ✅ `1.2.0` | ✅ `1.2.0` |
| `test_comparison_with_v1_1` | ✅ Old vs new differ | ✅ ✅ |

> Note: The exact confidence scores may vary slightly with the generated model, but they are reliably above the threshold in the fixed version.

---

## ⚠️ Regression prevention

- `preprocess_image()` is now explicitly documented and contains a test asserting the normalized range.
- The test suite ensures that preprocessed values fall in `[0, 1]` and that predictions are correct for the provided images.
- Example test added to compare against the buggy v1.1 implementation to guard against regressions.

---

## 📚 References

- `issue_project/README.md` — description of the bug and how to reproduce it
- `tests/test_regression.py` — original failing regression tests
- `src/mnist_classifier.py` — fixed source code
