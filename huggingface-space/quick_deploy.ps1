# Quick Deploy Script untuk Windows PowerShell
# Usage: .\quick_deploy.ps1 your-username/space-name

param(
    [Parameter(Mandatory=$true)]
    [string]$SpaceRepo
)

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🚀 Quick Deploy to Hugging Face Spaces" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Target Space: $SpaceRepo" -ForegroundColor Yellow
Write-Host ""

# Check if huggingface-cli is installed
try {
    $null = huggingface-cli whoami 2>&1
    Write-Host "✅ Logged in to HuggingFace" -ForegroundColor Green
} catch {
    Write-Host "❌ huggingface-cli tidak ditemukan atau belum login" -ForegroundColor Red
    Write-Host "Install: pip install huggingface-hub[cli]" -ForegroundColor Yellow
    Write-Host "Login: huggingface-cli login" -ForegroundColor Yellow
    exit 1
}

# Create space
Write-Host ""
Write-Host "📦 Creating Space repository..." -ForegroundColor Cyan
try {
    huggingface-cli repo create $SpaceRepo --type space --space_sdk docker
    Write-Host "✅ Space created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Repository mungkin sudah ada" -ForegroundColor Yellow
}

# Initialize git if needed
if (-not (Test-Path ".git")) {
    Write-Host ""
    Write-Host "📝 Initializing git..." -ForegroundColor Cyan
    git init
    git add .
    git commit -m "Initial commit: IndoBERT Fake News Detection"
}

# Add remote
Write-Host ""
Write-Host "🔗 Adding remote..." -ForegroundColor Cyan
$SpaceUrl = "https://huggingface.co/spaces/$SpaceRepo"
git remote remove origin 2>$null
git remote add origin $SpaceUrl

# Push
Write-Host ""
Write-Host "📤 Pushing to Hugging Face Spaces..." -ForegroundColor Cyan
git push -u origin main -f

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "✅ Deploy berhasil!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Space URL: $SpaceUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "ℹ️  Next steps:" -ForegroundColor Yellow
Write-Host "1. Tunggu build selesai (~5-10 menit)"
Write-Host "2. Cek status di: $SpaceUrl"
Write-Host "3. Set environment variables jika perlu (HF_MODEL_REPO)"
Write-Host ""
