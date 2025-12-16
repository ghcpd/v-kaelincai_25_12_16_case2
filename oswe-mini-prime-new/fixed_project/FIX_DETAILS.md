# FIX DETAILS — MNIST Classifier v1.2

## Bug Summary
The v1.1 release accidentally removed pixel normalization (`img = img / 255.0`) in
`preprocess_image()`. Models are trained on pixels normalized to `[0, 1]`, so passing
raw `[0, 255]` inputs causes incorrect predictions and unstable confidences.

## Root Cause Analysis
- In v1.0, images were normalized to the [0, 1] range before flattening.
- During an update to v1.1, the normalization line was removed, leaving raw values.
- This scaling mismatch between training and inference leads to incorrect logits
  and bad probabilities.

## Fix Implementation
Implemented a one-line fix in `src/mnist_classifier.py`:

```python
# Restore normalization to ensure inputs match training range
img = img / 255.0
```
Updated `VERSION = "1.2.0"` and added comments explaining the change.

## Verification: Test Results
All tests in `tests/test_fixed.py` pass (7/7):

| Metric | v1.1 (Bug) | v1.2 (Fixed) |
|--------|------------|--------------|
| Test Pass Rate | 2/7 (sanity checks only) | 7/7 ✅ |
| Digit 7 Prediction | ❌ Wrong/Low confidence | ✅ Correct (confidence > 0.5) |
| Digit 3 Prediction | ❌ Wrong | ✅ Correct |
| Preprocessing Range | [0, 255] | [0, 1] ✅ |

## Regression Prevention
- Add unit tests that explicitly check preprocessing range (`test_preprocessing_normalization_fixed`).
- Add brief comment in `preprocess_image()` documenting importance of normalization.
- Include simple data generation script so tests are reproducible.

## Notes
- The fix is intentionally minimal and localized to `preprocess_image()`.
- `generate_test_data.py` produces deterministic model and images for local testing.
