# Auto-run test script for MNIST classifier v1.2 (PowerShell)

Write-Host "=== MNIST Classifier v1.2 - Fixed Version ===" -ForegroundColor Green

# Install dependencies
Write-Host "\nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q

# Generate test data
Write-Host "\nGenerating test data..." -ForegroundColor Yellow
python generate_test_data.py

# Run tests
Write-Host "\nRunning tests..." -ForegroundColor Yellow
pytest tests/test_fixed.py -v --tb=short

Write-Host "\n=== All tests should pass! ===" -ForegroundColor Green
