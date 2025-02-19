@echo off
echo Installing Code Prompt Optimizer...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed! Please install pip.
    echo Visit: https://pip.pypa.io/en/stable/installation/
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
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
if errorlevel 1 (
    echo Failed to download NLTK data!
    pause
    exit /b 1
)

:: Run setup
echo Running setup...
python setup.py install
if errorlevel 1 (
    echo Failed to run setup!
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo To start the application, run: python token_script_v2.py
echo.
pause
