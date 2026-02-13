@echo off
echo === Patchwork Audio Setup ===
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo + Python found

REM Check for FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ! FFmpeg not found.
    echo.
    echo Please install FFmpeg:
    echo   - Download from https://ffmpeg.org/download.html
    echo   - Add to PATH environment variable
    echo.
    pause
    exit /b 1
)

echo + FFmpeg found

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create directories
echo.
echo Creating project directories...
if not exist downloads mkdir downloads
if not exist output mkdir output

REM Copy env example
if not exist .env (
    echo.
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo ! Remember to add your GENIUS_API_TOKEN to .env
)

echo.
echo === Setup Complete! ===
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the application, use:
echo   python main.py
echo.
pause
