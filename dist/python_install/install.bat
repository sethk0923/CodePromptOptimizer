@echo off
echo Installing Code Prompt Optimizer (Python Version)...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or newer from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Initialize tiktoken (this will download required encodings)
echo Initializing tiktoken...
python -c "import tiktoken; tiktoken.encoding_for_model('gpt-3.5-turbo')"
if errorlevel 1 (
    echo Warning: Failed to initialize tiktoken encodings
    echo You may need to run the application once to download required files
)

REM Initialize NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
if errorlevel 1 (
    echo Warning: Failed to download NLTK data
    echo You may need to run the application once to download required files
)

echo.
echo Installation complete!
echo To run the application, use: python token_script_v2.py
echo.
pause 