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
