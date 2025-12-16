# MNIST Classifier - Fixed Version v1.2.0

Overview
--------
This repository contains a fixed version (v1.2.0) of the MNIST handwritten digit classifier originally provided in `issue_project` (v1.1). The core bug was a missing pixel normalization step in preprocessing, which caused predictions to be incorrect.

Quick Start
-----------
1. Install dependencies:
   pip install -r requirements.txt
2. Generate test data (copies model/images from issue_project or synthesizes them):
   python generate_test_data.py
3. Run tests:
   pytest tests/test_fixed.py -v

Fix Summary
-----------
- Restored normalization in src/mnist_classifier.py: `img = img / 255.0`
- Updated VERSION to `1.2.0`

Testing & Verification
----------------------
All tests in `tests/test_fixed.py` verify predictions, preprocessing range, confidence, batch consistency, and include a comparison with v1.1 behavior.

Comparison with v1.1
--------------------
v1.1 had missing normalization and failed multiple regression tests. v1.2 restores preprocessing and passes all tests.

See FIX_DETAILS.md for a detailed report.
