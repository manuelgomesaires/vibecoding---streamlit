#!/bin/bash
# Setup script for Python Virtual Environment (Mac/Linux)
# Run this script to set up your development environment

echo ""
echo "🔧 Setting up Python development environment..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo ""
    echo "Please install Python first:"
    echo "  • Mac: Install from https://www.python.org/downloads/"
    echo "         Or use: brew install python3"
    echo "  • Linux: sudo apt install python3 python3-venv"
    echo ""
    exit 1
fi

echo "✅ Python found!"
python3 --version
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

if [ ! -d ".venv" ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created!"
echo ""

# Activate and install packages
echo "📦 Installing required packages..."
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete! 🎉"
echo ""
echo "Next steps:"
echo "  • Open this folder in VSCode (or Cursor)"
echo "  • Open a new terminal"
echo "  • Run: python main.py"
echo ""
echo "Your virtual environment will activate automatically in VSCode!"
echo ""

