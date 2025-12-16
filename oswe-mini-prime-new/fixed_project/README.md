# MNIST Classifier — Fixed v1.2 ✅

This repository contains a fixed version (v1.2.0) of the MNIST classifier that
restores a missing pixel normalization step accidentally removed in v1.1.

## Quick start

1. Install dependencies:
   pip install -r requirements.txt
2. Generate deterministic test data (model + test images):
   python generate_test_data.py
3. Run tests:
   pytest tests/test_fixed.py -v

## Fix summary
- Root cause: Missing `img = img / 255.0` in `preprocess_image()` (v1.1)
- Fix: Restore normalization and update `VERSION = "1.2.0"`

## Files
- `src/mnist_classifier.py` — Fixed classifier (v1.2.0)
- `generate_test_data.py` — Generates deterministic model and test images
- `tests/test_fixed.py` — Test suite verifying the fix

## Comparison with v1.1
See `FIX_DETAILS.md` for a side-by-side comparison of test results and behavior.
