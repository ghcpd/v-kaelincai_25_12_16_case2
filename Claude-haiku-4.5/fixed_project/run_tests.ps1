# MNIST Classifier v1.2 - Fixed Version Test Runner
# PowerShell Script for Windows

# Display header
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   MNIST Classifier v1.2 - Fixed Version Test Suite   ║" -ForegroundColor Cyan
Write-Host "║                    All Tests Should Pass              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install dependencies
Write-Host "📦 Step 1: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 2: Generate test data
Write-Host "🎨 Step 2: Generating test data..." -ForegroundColor Yellow
python generate_test_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to generate test data" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 3: Run tests
Write-Host "🧪 Step 3: Running tests (7 tests expected to pass)..." -ForegroundColor Yellow
Write-Host ""
pytest tests/test_fixed.py -v --tb=short
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Some tests failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Success message
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ✅ ALL TESTS PASSED (7/7)               ║" -ForegroundColor Green
Write-Host "║            v1.2 Fix Successfully Applied             ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "  ✅ Dependencies installed"
Write-Host "  ✅ Test data generated"
Write-Host "  ✅ All 7 tests passing"
Write-Host "  ✅ Preprocessing normalization verified"
Write-Host "  ✅ Digit predictions correct (7, 3, etc.)"
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  - README.md          — Quick start and overview"
Write-Host "  - FIX_DETAILS.md     — Detailed technical analysis"
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Review FIX_DETAILS.md for the technical explanation"
Write-Host "  2. Examine the fix in src/mnist_classifier.py (line 55)"
Write-Host "  3. Run individual tests: pytest tests/test_fixed.py::TestDigitPredictionFixed -v"
Write-Host ""
