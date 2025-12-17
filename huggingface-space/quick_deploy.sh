#!/bin/bash

# Quick Deploy Script untuk Hugging Face Space
# Usage: ./quick_deploy.sh your-username/space-name

set -e

SPACE_REPO=$1

if [ -z "$SPACE_REPO" ]; then
    echo "❌ Error: Space repository tidak diberikan"
    echo "Usage: ./quick_deploy.sh your-username/space-name"
    exit 1
fi

echo "=================================================="
echo "🚀 Quick Deploy to Hugging Face Spaces"
echo "=================================================="
echo "Target Space: $SPACE_REPO"
echo ""

# Check if huggingface-cli is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo "❌ huggingface-cli tidak ditemukan"
    echo "Install dengan: pip install huggingface-hub[cli]"
    exit 1
fi

# Check if logged in
echo "🔐 Checking HuggingFace login..."
if ! huggingface-cli whoami &> /dev/null; then
    echo "⚠️  Anda belum login ke HuggingFace"
    echo "Silakan login terlebih dahulu:"
    huggingface-cli login
fi

echo "✅ Logged in"

# Create space if not exists
echo ""
echo "📦 Creating Space repository..."
huggingface-cli repo create "$SPACE_REPO" --type space --space_sdk docker || echo "Repository mungkin sudah ada"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo ""
    echo "📝 Initializing git..."
    git init
    git add .
    git commit -m "Initial commit: IndoBERT Fake News Detection"
fi

# Add remote
echo ""
echo "🔗 Adding remote..."
SPACE_URL="https://huggingface.co/spaces/$SPACE_REPO"
git remote remove origin 2>/dev/null || true
git remote add origin "$SPACE_URL"

# Push
echo ""
echo "📤 Pushing to Hugging Face Spaces..."
git push -u origin main -f

echo ""
echo "=================================================="
echo "✅ Deploy berhasil!"
echo "=================================================="
echo ""
echo "🔗 Space URL: $SPACE_URL"
echo ""
echo "ℹ️  Next steps:"
echo "1. Tunggu build selesai (~5-10 menit)"
echo "2. Cek status di: $SPACE_URL"
echo "3. Set environment variables jika perlu (HF_MODEL_REPO)"
echo ""
