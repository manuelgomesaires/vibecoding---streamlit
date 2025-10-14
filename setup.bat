@echo off
REM Windows Setup Script for Python Virtual Environment
REM Double-click this file or run from Command Prompt

echo.
echo 🔧 Setting up Python development environment for Windows...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    echo.
    echo Please install Python first:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.x
    echo 3. During installation, CHECK "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
python --version
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

if not exist .venv\Scripts\activate.bat (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created!
echo.

REM Activate and install packages
echo 📦 Installing required packages...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ Setup complete! 🎉
echo.
echo Next steps:
echo 1. Open this folder in VSCode (or Cursor)
echo 2. Open a new terminal
echo 3. Run: python main.py
echo.
pause

