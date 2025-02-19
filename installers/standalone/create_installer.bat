@echo off
setlocal enabledelayedexpansion

echo Creating standalone installer for Code Prompt Optimizer...
echo.

:: Check Python version
for /f "tokens=2 delims=." %%a in ('python -V 2^>^&1') do set pyver=%%a
if %pyver% LSS 8 (
    echo Error: Python 3.8 or higher is required to create the installer.
    echo Current version: !pyver!
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

:: Check if NSIS is installed
makensis /VERSION >nul 2>&1
if errorlevel 1 (
    echo Error: NSIS is not installed!
    echo Please download and install NSIS from https://nsis.sourceforge.io/Download
    echo Make sure to add NSIS to your system PATH
    pause
    exit /b 1
)

:: Create the installer
echo Creating installer...
python create_installers.py
if errorlevel 1 (
    echo Failed to create installer!
    pause
    exit /b 1
)

echo.
echo Installer creation completed!
echo Check the windows/output directory for the installer.
echo.
pause 