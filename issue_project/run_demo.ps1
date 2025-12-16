# Quick Start Script for MNIST Classifier Regression Bug Project (PowerShell)
# ==============================================================

Write-Host ""
Write-Host "========================================"
Write-Host "MNIST Classifier v1.1 Regression Demo"
Write-Host "========================================"
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion"
} catch {
    Write-Host "ERROR: Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[1/3] Installing dependencies..."
python -m pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "[2/3] Generating test data..."
python generate_test_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to generate test data." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/3] Running regression tests..."
Write-Host ""
Write-Host "NOTE: Some tests WILL FAIL - this demonstrates the regression bug!" -ForegroundColor Yellow
Write-Host ""
python -m pytest tests/test_regression.py -v --tb=short

Write-Host ""
Write-Host "========================================"
Write-Host "Demo Complete!"
Write-Host "========================================"
Write-Host ""
Write-Host "The test failures above demonstrate the normalization bug in v1.1."
Write-Host "See KNOWN_ISSUE.md for detailed analysis and fix instructions."
Write-Host ""
