@echo off
echo Installing Code Prompt Optimizer...
echo.

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.7 or newer from python.org
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

:: Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Install required packages
echo Installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Install NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

:: Create executable
echo Creating executable...
pyinstaller --onefile --windowed --icon=icon.ico --name=CodePromptOptimizer token_script_v2.py

:: Copy executable to Desktop
echo Copying executable to Desktop...
copy /Y "dist\CodePromptOptimizer.exe" "%USERPROFILE%\Desktop\"

echo.
echo Installation complete! You can find CodePromptOptimizer.exe on your Desktop.
echo Press any key to exit...
pause > nul
