@echo off
REM AI Programming Tool - Windows Environment Setup Script
REM This script sets up the Python virtual environment and installs dependencies

echo 🚀 Setting up AI Programming Tool environment...

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ℹ️  Detected Python version: %PYTHON_VERSION%

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ℹ️  Virtual environment already exists
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
if exist "requirements.txt" (
    echo 📥 Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    echo ✅ Dependencies installed successfully
) else (
    echo ❌ Error: requirements.txt not found
    deactivate
    pause
    exit /b 1
)

REM Verify PyQt5 installation
echo 🔍 Verifying PyQt5 installation...
python -c "import PyQt5; print('PyQt5 version:', PyQt5.__version__)"

REM Verify Pygments installation
echo 🔍 Verifying Pygments installation...
python -c "import pygments; print('Pygments version:', pygments.__version__)"

echo.
echo 🎉 Environment setup completed successfully!
echo.
echo To activate the environment manually, run:
echo   venv\Scripts\activate
echo.
echo To run the AI Programming Tool:
echo   python ai_programming_tool.py
echo.
echo To deactivate the environment:
echo   deactivate
echo.
pause
