# PowerShell installer for ALPHA_BOT (Windows)
set -e
$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Installing ALPHA_BOT into: $Root"

# Create virtual environment
if (-not (Test-Path "$Root\.venv")) {
    python -m venv "$Root\.venv"
}

# Activate and install
& "$Root\.venv\Scripts\python.exe" -m pip install --upgrade pip
& "$Root\.venv\Scripts\python.exe" -m pip install -r "$Root\requirements.txt"

# Copy .env if not exists
if (-not (Test-Path "$Root\.env")) {
    Copy-Item "$Root\.env.example" "$Root\.env"
    Write-Host ".env created from .env.example — edit it and add your TELEGRAM_TOKEN"
}

Write-Host "Installation complete. To run the bot:"
Write-Host ". $Root\\.venv\\Scripts\\Activate.ps1"
Write-Host "python $Root\\main.py"
