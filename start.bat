@echo off
echo ================================================
echo PDF Classifier - Quick Start Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Checking Python...
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo [2/5] Creating virtual environment...
    python -m venv venv
) else (
    echo.
    echo [2/5] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo [4/5] Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found
    echo Copying .env.example to .env...
    copy .env.example .env
    echo Please edit .env with your configuration
)

REM Initialize application
echo.
echo [5/5] Initializing application...
python init.py

REM Optional: regenerate static HTML docs (can be skipped with 'nogen' arg)
if not "%1"=="nogen" (
    if exist "tools\gen_docs.bat" (
        echo Regenerating manual HTML files...
        call tools\gen_docs.bat
    ) else (
        echo tools\gen_docs.bat not found; skipping documentation generation
    )
) else (
    echo Skipping docs generation (nogen)
)

echo.
echo ================================================
echo Setup completed!
echo ================================================
echo.
echo To start the application, run:
echo   python app.py
echo.
echo Then open your browser at: http://localhost:5000
echo ================================================
pause
