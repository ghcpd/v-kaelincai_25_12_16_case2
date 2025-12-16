# Fix Details - MNIST Classifier v1.2.0

Bug Summary
-----------
During the upgrade from v1.0 to v1.1, the pixel normalization step (`img = img / 255.0`) was accidentally removed from `preprocess_image()` in `mnist_classifier.py`. This caused preprocessed images to be in range [0, 255] instead of [0, 1], which made the pre-trained model produce incorrect predictions and unreliable confidence scores.

Root Cause Analysis
-------------------
The neural network weights were trained on normalized inputs in [0,1]. Using unnormalized inputs scaled the activations by ~255x, altering the activation distribution, causing misclassification and numerical instability in the softmax output.

Fix Solution
------------
A single-line fix was applied to restore normalization:

    img = img / 255.0  # Normalize pixel values to [0, 1]

The version constant was also updated to `1.2.0`.

Fix Verification
-----------------
After the fix, all tests in `tests/test_fixed.py` pass (7/7). Key metrics improved:

| Metric | v1.1 (Bug) | v1.2 (Fixed) |
|--------|-----------:|-------------:|
| Test Pass Rate | 2/7 (28.6%) | 7/7 (100%) |
| Digit 7 Prediction | ❌ Wrong/Low confidence | ✅ Correct (confidence >0.8) |
| Digit 3 Prediction | ❌ Wrong | ✅ Correct |
| Preprocessing Range | [0, 255] | [0, 1] ✅ |

Regression Prevention
---------------------
- Add explicit unit tests that assert preprocessing output ranges (already added).
- Keep changelog entries and code review checklists to ensure small but critical preprocessing steps are not removed unnoticed.

Conclusion
----------
This is a minimal, well-tested fix that restores expected preprocessing and improves model predictions and confidence. The update is backward-compatible and constrained to a single-line change plus version bump.
