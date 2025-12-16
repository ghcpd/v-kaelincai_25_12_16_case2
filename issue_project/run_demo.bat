@echo off
REM Quick Start Script for MNIST Classifier Regression Bug Project
REM ==============================================================

echo.
echo ========================================
echo MNIST Classifier v1.1 Regression Demo
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ first.
    exit /b 1
)

echo [1/3] Installing dependencies...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [2/3] Generating test data...
python generate_test_data.py
if errorlevel 1 (
    echo ERROR: Failed to generate test data.
    exit /b 1
)

echo.
echo [3/3] Running regression tests...
echo.
echo NOTE: Some tests WILL FAIL - this demonstrates the regression bug!
echo.
python -m pytest tests/test_regression.py -v --tb=short

echo.
echo ========================================
echo Demo Complete!
echo ========================================
echo.
echo The test failures above demonstrate the normalization bug in v1.1.
echo See KNOWN_ISSUE.md for detailed analysis and fix instructions.
echo.

pause
