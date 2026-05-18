#!/bin/bash

# SimplifiQ Setup Script
# This script helps you set up the project with minimal hassle

set -e

echo "=========================================="
echo "SimplifiQ AI Lead Automation - Setup"
echo "=========================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "  Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
echo "  ✓ Virtual environment activated"
echo ""

# Install dependencies
echo "✓ Installing Python dependencies..."
pip install -q -r requirements.txt
echo "  All dependencies installed"
echo ""

# Create .env file if it doesn't exist
echo "✓ Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  Created .env file (edit with your credentials)"
else
    echo "  .env file already exists"
fi
echo ""

# Create directories
mkdir -p reports templates

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your credentials:"
echo "   - OPENAI_API_KEY"
echo "   - SENDER_EMAIL & SENDER_PASSWORD"
echo ""
echo "2. Start the server:"
echo "   python main.py"
echo ""
echo "3. Open your browser:"
echo "   http://localhost:8000"
echo ""
echo "📖 For detailed setup instructions, see README.md"
echo ""