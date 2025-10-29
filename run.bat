@echo off
echo Starting PDF Classifier...
echo.

REM Optional flag: run.bat nogen  -> skip regenerating docs
if "%1"=="nogen" (
    echo Skipping docs regeneration (nogen flag present)
    goto skip_gen
)

REM Regenerate static HTML docs from manual/*.md
if exist "tools\gen_docs.bat" (
    echo Regenerating manual HTML files...
    call tools\gen_docs.bat
) else (
    echo tools\gen_docs.bat not found, skipping documentation generation
)

:skip_gen

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Start the application
echo Starting Flask application...
echo Access at: http://localhost:5000
echo Press CTRL+C to stop
echo.

python app.py
