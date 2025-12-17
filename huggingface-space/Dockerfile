# Hugging Face Space - IndoBERT Fake News Detection
# Base image dengan Python 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first untuk caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (hanya file yang diperlukan)
COPY app.py .

# Model akan di-load dari HuggingFace Hub, tidak perlu copy lokal
# Environment variable HF_MODEL_REPO akan di-set di Space settings

# Expose port 7860 (default untuk HF Spaces)
EXPOSE 7860

# Set environment variables
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860
ENV HF_MODEL_REPO="Davidbio/fakenewsdetection"

# Run the application
CMD ["python", "app.py"]
