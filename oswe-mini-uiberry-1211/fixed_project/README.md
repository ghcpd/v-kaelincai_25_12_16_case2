# MNIST Classifier — Fixed Version (v1.2)

This repository contains the fixed version (v1.2.0) of a simple MNIST
handwritten-digit classifier. The v1.1 release accidentally removed a
critical preprocessing step (pixel normalization). This fixed project
restores that step and includes tests and scripts to verify the fix.

Quick start
----------
1. Create a virtual environment (recommended) and activate it.
2. Install dependencies:
   pip install -r requirements.txt
3. Generate model and test images:
   python generate_test_data.py
4. Run tests:
   pytest tests/test_fixed.py -v

What was fixed
--------------
- Restored `img = img / 255.0` in preprocess_image() so inputs are in [0,1].
- Updated VERSION to `1.2.0`.
- Added tests that validate normalization, predictions, and confidence.

Files of interest
-----------------
- src/mnist_classifier.py (fixed classifier)
- generate_test_data.py (creates models/ and data/)
- tests/test_fixed.py (7 tests, all should pass)
- FIX_DETAILS.md (detailed fix report)

Comparison with v1.1
--------------------
v1.1 suffered from missing normalization and failed 5 of 7 tests.
v1.2 restores normalization and should pass all tests (7/7).

License / Notes
----------------
This is a small demonstration project for educational purposes.
