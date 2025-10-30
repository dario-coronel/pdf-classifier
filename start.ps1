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

if (-not $NoGen) {
    Write-Host "`nRegenerating manual HTML files (this may take a moment)..." -ForegroundColor Green
    # Prefer using the Python converter to avoid shell-specific issues
    python tools\md_to_html.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: Failed to regenerate manual HTML (exit code $LASTEXITCODE)" -ForegroundColor Yellow
    } else {
        Write-Host "Docs generated in manual/html" -ForegroundColor Green
    }
} else {
    Write-Host "Skipping docs regeneration (-NoGen specified)." -ForegroundColor Cyan
}

Write-Host "`nSetup completed. To start the app run:`n    python app.py" -ForegroundColor Cyan
Write-Host "Open your browser at http://localhost:5000" -ForegroundColor Cyan
Write-Host "===============================================`n" -ForegroundColor Cyan

Pause
