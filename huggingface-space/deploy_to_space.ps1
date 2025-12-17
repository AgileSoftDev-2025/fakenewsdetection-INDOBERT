# Deploy to HuggingFace Space - Script Otomatis
# Usage: .\deploy_to_space.ps1

$SpaceRepo = "Davidbio/fakenewsdetection"
$SpaceUrl = "https://huggingface.co/spaces/$SpaceRepo"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🚀 Deploy to HuggingFace Space" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Space: $SpaceRepo" -ForegroundColor Yellow
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

# Create temporary directory
$TempDir = "temp_space_deploy"
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}

Write-Host ""
Write-Host "📦 Cloning Space repository..." -ForegroundColor Cyan
git clone $SpaceUrl $TempDir

if (-not (Test-Path $TempDir)) {
    Write-Host "❌ Failed to clone Space" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Space cloned" -ForegroundColor Green

# Copy HANYA file yang diperlukan
Write-Host ""
Write-Host "📄 Copying files..." -ForegroundColor Cyan

$FilesToCopy = @(
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "README.md",
    ".dockerignore",
    ".gitignore"
)

foreach ($File in $FilesToCopy) {
    if (Test-Path $File) {
        Copy-Item $File $TempDir\ -Force
        Write-Host "  ✅ $File" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $File not found" -ForegroundColor Yellow
    }
}

# Commit dan push
Write-Host ""
Write-Host "📤 Pushing to Space..." -ForegroundColor Cyan

Set-Location $TempDir

git add .
git commit -m "Deploy: IndoBERT Fake News Detection (optimized, model from HF Hub)"
git push

Set-Location ..

# Cleanup
Write-Host ""
Write-Host "🧹 Cleaning up..." -ForegroundColor Cyan
Remove-Item $TempDir -Recurse -Force

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "✅ Deploy berhasil!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Space URL: $SpaceUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "ℹ️  Next steps:" -ForegroundColor Yellow
Write-Host "1. Tunggu build selesai (~3-5 menit)"
Write-Host "2. Cek status: $SpaceUrl"
Write-Host "3. Test aplikasi dengan contoh teks"
Write-Host "4. Monitor logs untuk debugging"
Write-Host ""
Write-Host "Model akan di-load dari: https://huggingface.co/Davidbio/fakenewsdetection" -ForegroundColor Cyan
Write-Host ""
