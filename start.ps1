<#
.SYNOPSIS
    Script de inicio en PowerShell para PDF Classifier.

.DESCRIPTION
    Crea/activa el virtualenv, instala dependencias, inicializa la app y (por defecto)
    regenera la documentación estática (manual/html). Use -NoGen para omitir.

.EXAMPLE
    .\start.ps1
    .\start.ps1 -NoGen
#>

param(
    [switch]$NoGen
)

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "PDF Classifier - Quick Start (PowerShell)" -ForegroundColor Cyan
Write-Host "===============================================`n"

Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
try {
    $py = & python --version 2>$null
    Write-Host "Python detected: $py"
} catch {
    Write-Host "ERROR: Python not found or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
}

Write-Host "`n[2/6] Checking/creating virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path -Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
} else {
    Write-Host "Virtual environment already exists."
}

Write-Host "`n[3/6] Activating virtual environment..." -ForegroundColor Yellow
$activate = Join-Path -Path "venv" -ChildPath "Scripts/Activate.ps1"
if (Test-Path $activate) {
    Write-Host "Using: $activate"
    & $activate
} else {
    Write-Host "ERROR: Activate.ps1 not found in venv\Scripts" -ForegroundColor Red
    exit 1
}

Write-Host "`n[4/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`n[5/6] Checking .env..." -ForegroundColor Yellow
if (-not (Test-Path -Path ".env")) {
    Write-Host ".env not found. Copying .env.example to .env"
    Copy-Item -Path ".env.example" -Destination ".env"
    Write-Host "Please review .env and update credentials as needed."
}

Write-Host "`n[6/6] Initializing application..." -ForegroundColor Yellow
python init.py

Write-Host "`nNote: Automatic docs regeneration has been disabled to restore previous behavior."
Write-Host "If you need to regenerate the manual HTML files, run: python tools\md_to_html.py or tools\gen_docs.bat" -ForegroundColor Yellow

Write-Host "`nSetup completed. To start the app run:`n    python app.py" -ForegroundColor Cyan
Write-Host "Open your browser at http://localhost:5000" -ForegroundColor Cyan
Write-Host "===============================================`n" -ForegroundColor Cyan

Pause
