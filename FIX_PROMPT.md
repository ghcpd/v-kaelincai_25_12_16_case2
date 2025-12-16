# Project Fix Prompt - MNIST Classifier v1.2

## Role & Scope
**Role**: Senior Software Engineer and Fix Specialist  
**Mission**: Analyze existing issue_project (v1.1 with regression bug) and create fixed version (v1.2)  
**Workspace**: Create new project folder named `fixed_project` in current workspace

---

## Project Background

### Original Project Overview
`issue_project` is an MNIST handwritten digit classifier project with a **deliberately injected preprocessing regression bug** for demonstration and testing purposes.

**Current Version**: v1.1 (contains bug)  
**Project Type**: Python Machine Learning Classifier  
**Bug Type**: Preprocessing regression — missing pixel normalization step

### Issue Details

#### Bug Location
- **File**: `src/mnist_classifier.py`
- **Class**: `MNISTClassifier`
- **Method**: `preprocess_image()`
- **Lines**: Approximately 45-48

#### Root Cause
During the v1.0 to v1.1 upgrade, the **pixel normalization step was accidentally removed** (`img = img / 255.0`), causing:
- **Expected input range**: `[0, 1]` (used during model training)
- **Actual input range**: `[0, 255]` (unnormalized)
- **Impact**: All predictions are inaccurate with abnormal confidence levels

#### Buggy Code (v1.1)
```python
def preprocess_image(self, image_path):
    img = Image.open(image_path).convert('L')
    if img.size != (28, 28):
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    img = np.array(img)
    # ❌ Missing: img = img / 255.0  # Normalize to [0, 1]
    img = img.flatten()
    
    return img
```

#### Test Failure Status
Out of 7 automated tests:
- ❌ **5 tests fail** (critical tests)
  - `test_predict_digit_7_with_confidence` — Confidence too low
  - `test_preprocessing_output_range` — Output range wrong (critical)
  - `test_batch_prediction_consistency` — Predictions inconsistent
  - `test_predict_digit_3_basic` — Wrong prediction
- ✅ **2 tests pass** (sanity checks)
  - `test_model_loads_successfully` — Model loads fine
  - `test_version_is_v1_1` — Version check

---

## Fix Requirements

### 1. Core Fix ✅
**Fix the bug in `fixed_project/src/mnist_classifier.py`**:

```python
def preprocess_image(self, image_path):
    img = Image.open(image_path).convert('L')
    if img.size != (28, 28):
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    img = np.array(img)
    img = img / 255.0  # ✅ Restore normalization step
    img = img.flatten()
    
    return img
```

**Key Points**:
- Update version to `VERSION = "1.2.0"`
- Add clear comments explaining the fix
- Keep all other code unchanged

### 2. Project Structure ✅
Create complete fixed project structure:

```
fixed_project/
├── src/
│   ├── __init__.py
│   └── mnist_classifier.py        # Fixed classifier (v1.2)
├── tests/
│   ├── __init__.py
│   └── test_fixed.py              # Tests to verify fix (should all pass)
├── models/
│   └── mnist_model.npy            # Same pretrained model
├── data/
│   ├── test_digit_7.png           # Test image
│   └── test_digit_3.png           # Test image
├── generate_test_data.py          # Test data generation script
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── README.md                      # Usage guide
├── FIX_DETAILS.md                 # Fix documentation
└── run_tests.{bat,ps1}            # Quick test scripts
```

### 3. Test Requirements ✅
Create test suite in `fixed_project/tests/test_fixed.py`:

**Required Tests**:
1. ✅ `test_predict_digit_7_fixed` — Verify digit 7 prediction correct
2. ✅ `test_predict_digit_3_fixed` — Verify digit 3 prediction correct
3. ✅ `test_preprocessing_normalization_fixed` — Verify normalization range [0, 1]
4. ✅ `test_confidence_high_for_correct_predictions` — Verify high confidence (>0.5)
5. ✅ `test_batch_prediction_fixed` — Verify batch prediction consistency
6. ✅ `test_version_is_v1_2` — Verify version is 1.2.0
7. ✅ `test_comparison_with_v1_1` — Comparison test (show fix effect)

**Expected Result**: All 7 tests should pass ✅

### 4. Documentation Requirements ✅

#### README.md
Include the following sections:
- Project overview (emphasize this is fixed version of v1.1)
- Quick start guide
- Fix summary (brief)
- Test execution instructions
- Comparison with v1.1

#### FIX_DETAILS.md
Detailed fix report containing:
- **Bug Summary**: Problem description and impact
- **Root Cause Analysis**: Technical details and numerical examples
- **Fix Solution**: Code change explanation
- **Fix Verification**: Test result comparison tables
- **Regression Prevention**: How to prevent such issues from recurring

Comparison table example:
```markdown
| Metric | v1.1 (Bug) | v1.2 (Fixed) |
|--------|-----------|--------------|
| Test Pass Rate | 2/7 (28.6%) | 7/7 (100%) |
| Digit 7 Prediction | ❌ Wrong/Low confidence | ✅ Correct (confidence >0.8) |
| Digit 3 Prediction | ❌ Wrong | ✅ Correct |
| Preprocessing Range | [0, 255] | [0, 1] ✅ |
```

### 5. One-Click Run Scripts ✅

#### PowerShell Script (`run_tests.ps1`)
```powershell
# Automatically install dependencies, generate data, run tests and show results
Write-Host "=== MNIST Classifier v1.2 - Fixed Version ===" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q

# Generate test data
Write-Host "Generating test data..." -ForegroundColor Yellow
python generate_test_data.py

# Run tests
Write-Host "`nRunning tests..." -ForegroundColor Yellow
pytest tests/test_fixed.py -v --tb=short

# Show summary
Write-Host "`n=== All tests should pass! ===" -ForegroundColor Green
```

#### Batch Script (`run_tests.bat`)
```batch
@echo off
echo === MNIST Classifier v1.2 - Fixed Version ===
echo.
echo Installing dependencies...
pip install -r requirements.txt -q

echo Generating test data...
python generate_test_data.py

echo.
echo Running tests...
pytest tests/test_fixed.py -v --tb=short

echo.
echo === All tests should pass! ===
pause
```

---

## Quality Standards

### Code Quality
- ✅ Follow original project's code style
- ✅ Add clear comments (English or Chinese both acceptable)
- ✅ Keep code clean and understandable
- ✅ Don't add unnecessary complexity

### Test Coverage
- ✅ 100% test pass rate
- ✅ Cover all critical functionality
- ✅ Include comparison tests (v1.1 vs v1.2)
- ✅ Clear assertion error messages

### Documentation Completeness
- ✅ README includes quick start guide
- ✅ FIX_DETAILS includes detailed technical analysis
- ✅ Code comments explain fixes
- ✅ Include comparison tables and diagrams (if applicable)

---

## Output Format

### Creation Order
1. Create project directory structure
2. Copy and fix core code (`mnist_classifier.py`)
3. Create test suite (`test_fixed.py`)
4. Create documentation (`README.md`, `FIX_DETAILS.md`)
5. Create run scripts (`.ps1`, `.bat`)
6. Copy support files (`generate_test_data.py`, `requirements.txt`, etc.)

### Completion Criteria
1. ✅ All files created
2. ✅ Run `pytest tests/test_fixed.py -v` shows 7/7 passing
3. ✅ Run `run_tests.ps1` or `run_tests.bat` completes successfully
4. ✅ Documentation is complete and accurate

---

## Reference Materials

### Original Issue Project Location
- Path: `issue_project/`
- Key files:
  - `issue_project/src/mnist_classifier.py` — Buggy source code
  - `issue_project/tests/test_regression.py` — Failing tests
  - `issue_project/KNOWN_ISSUE.md` — Detailed issue description

### Technical Constraints
- Python 3.8+
- Windows 11 / PowerShell
- Dependencies: numpy, pillow, pytest

---

## Important Notes

1. **Do NOT modify original `issue_project`** — Create new `fixed_project` folder
2. **Keep it simple** — This is a one-line fix, don't over-engineer
3. **Test-first** — Ensure all tests pass before completion
4. **Clear documentation** — Enable users to quickly understand fix and verification
5. **Repeatability** — Ensure one-click scripts work in fresh environments

---

## Expected Outcome

Upon completion, users should be able to:
1. Run `cd fixed_project && .\run_tests.ps1`
2. See all 7 tests pass ✅
3. Understand what the v1.1 bug was and how v1.2 fixes it
4. Compare performance differences between v1.1 and v1.2

**Success Indicator**: From failing tests (5/7) to all tests passing (7/7), clearly demonstrating the fix effect.
