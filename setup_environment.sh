#!/bin/bash
# AI Programming Tool - Environment Setup Script
# This script sets up the Python virtual environment and installs dependencies

set -e  # Exit on error

echo "🚀 Setting up AI Programming Tool environment..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.8"

if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]]; then
    echo "❌ Error: Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version check passed: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📥 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error: requirements.txt not found"
    deactivate
    exit 1
fi

# Verify PyQt5 installation
echo "🔍 Verifying PyQt5 installation..."
python3 -c "import PyQt5; print(f'PyQt5 version: {PyQt5.__version__}')"

# Verify Pygments installation
echo "🔍 Verifying Pygments installation..."
python3 -c "import pygments; print(f'Pygments version: {pygments.__version__}')"

echo ""
echo "🎉 Environment setup completed successfully!"
echo ""
echo "To activate the environment manually, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the AI Programming Tool:"
echo "  python ai_programming_tool.py"
echo ""
echo "To deactivate the environment:"
echo "  deactivate"
echo ""

# Keep environment activated for immediate use
echo "ℹ️  Virtual environment is now active. You can run the application directly."
