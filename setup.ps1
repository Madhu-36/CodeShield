Write-Host "🚀 Setting up CodeShield Project for Windows..." -ForegroundColor Green

# Create Virtual Environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Virtual Environment..."
    python -m venv venv
}

# Activate and Install
Write-Host "Activating Virtual Environment and installing dependencies..."
.\venv\Scripts\Activate.ps1
pip install -e .

# Setup .env
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "Created .env file. Please open it and add your OPENAI_API_KEY." -ForegroundColor Yellow
} else {
    Write-Host ".env file already exists."
}

Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "To start using CodeShield, run:" -ForegroundColor Cyan
Write-Host ".\venv\Scripts\Activate.ps1"
Write-Host "python cli.py --help"
