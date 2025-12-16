@echo off
REM MNIST Classifier v1.2 - Fixed Version Test Runner
REM Batch Script for Windows Command Prompt

echo.
echo ======================================================
echo   MNIST Classifier v1.2 - Fixed Version Test Suite
echo                All Tests Should Pass
echo ======================================================
echo.

REM Step 1: Install dependencies
echo [Step 1] Installing dependencies...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Step 2: Generate test data
echo [Step 2] Generating test data...
python generate_test_data.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate test data
    pause
    exit /b 1
)
echo.

REM Step 3: Run tests
echo [Step 3] Running tests (7 tests expected to pass)...
echo.
pytest tests/test_fixed.py -v --tb=short
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Some tests failed
    pause
    exit /b 1
)
echo.

REM Success message
echo ======================================================
echo   SUCCESS! All tests passed (7/7)
echo   v1.2 Fix Successfully Applied
echo ======================================================
echo.
echo Summary:
echo   [OK] Dependencies installed
echo   [OK] Test data generated
echo   [OK] All 7 tests passing
echo   [OK] Preprocessing normalization verified
echo   [OK] Digit predictions correct
echo.
echo Documentation:
echo   - README.md          - Quick start and overview
echo   - FIX_DETAILS.md     - Detailed technical analysis
echo.
echo Next Steps:
echo   1. Review FIX_DETAILS.md for the technical explanation
echo   2. Examine the fix in src\mnist_classifier.py (line 55)
echo   3. Run individual tests: pytest tests/test_fixed.py::TestDigitPredictionFixed -v
echo.
pause
