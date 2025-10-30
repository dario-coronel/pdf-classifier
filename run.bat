@echo off
echo Starting PDF Classifier...
echo.

REM Activate virtual environment (classic behavior - no doc regen)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run start.bat first
    pause
    exit /b 1
)

echo Starting Flask application...
echo Access at: http://localhost:5000
echo Press CTRL+C to stop
echo.

python app.py
