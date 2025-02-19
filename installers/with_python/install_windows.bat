@echo off
setlocal enabledelayedexpansion

echo Installing Code Prompt Optimizer (Python Version)...
echo.

:: Check Python version
for /f "tokens=2 delims=." %%a in ('python -V 2^>^&1') do set pyver=%%a
if %pyver% LSS 8 (
    echo Error: Python 3.8 or higher is required.
    echo Current version: !pyver!
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Install requirements
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements!
    pause
    exit /b 1
)

:: Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
if errorlevel 1 (
    echo Failed to download NLTK data!
    pause
    exit /b 1
)

:: Verify installation
echo Verifying installation...
python -c "import tkinter, tiktoken, nltk, requests"
if errorlevel 1 (
    echo Warning: Some packages may not be installed correctly.
    echo Please check the error messages above.
) else (
    echo All core packages verified successfully!
)

echo.
echo Installation completed!
echo To start the application: python token_script_v2.py
echo.

pause 