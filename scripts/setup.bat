@echo off
REM ###################################################
REM # setup.bat — Initial project setup (Windows)
REM # Creates virtual environment and installs dependencies
REM ###################################################

echo Setting up environment...

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo Setup complete. Run 'scripts\run.bat' to execute the pipeline.
