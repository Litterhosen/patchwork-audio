#!/bin/bash

echo "=== Patchwork Audio Setup ==="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check for FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found."
    echo ""
    echo "Please install FFmpeg:"
    echo "  - Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  - macOS: brew install ffmpeg"
    echo "  - Windows: Download from https://ffmpeg.org/download.html"
    echo ""
    exit 1
fi

echo "✓ FFmpeg found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
echo ""
echo "Creating project directories..."
mkdir -p downloads output

# Copy env example
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Remember to add your GENIUS_API_TOKEN to .env"
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the application, use:"
echo "  python main.py"
echo ""
