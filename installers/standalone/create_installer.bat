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

:: Check if NSIS is installed and set the path
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    set "NSIS_EXE=C:\Program Files (x86)\NSIS\makensis.exe"
) else (
    echo Error: NSIS is not installed!
    echo Please download and install NSIS from https://nsis.sourceforge.io/Download
    pause
    exit /b 1
)

:: Create the installer
echo Creating installer...
set "PATH=C:\Program Files (x86)\NSIS;%PATH%"
python create_installers.py --icon=../../assets/icon.ico
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
