# PowerShell helper to install deps, generate data and run tests
Write-Host "=== MNIST Classifier v1.2 - Fixed Version ===" -ForegroundColor Green

Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q

Write-Host "Generating test data..." -ForegroundColor Yellow
python generate_test_data.py

Write-Host "`nRunning tests..." -ForegroundColor Yellow
pytest tests/test_fixed.py -v --tb=short

Write-Host "`n=== All tests should pass! ===" -ForegroundColor Green
