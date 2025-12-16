@echo off
echo === MNIST Classifier v1.2 - Fixed Version ===

echo Installing dependencies...
python -m pip install -r requirements.txt -q


echo Generating test data...
python generate_test_data.py


echo Running tests...
python -m pytest tests/test_fixed.py -v --tb=short

pause
