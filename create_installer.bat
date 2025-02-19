@echo off
echo Creating Code Prompt Optimizer Installer...
echo.

REM Check if NSIS is installed
makensis -VERSION > nul 2>&1
if errorlevel 1 (
    echo Error: NSIS is not installed
    echo Please download and install NSIS from https://nsis.sourceforge.io/Download
    echo Make sure to add NSIS to your system PATH
    pause
    exit /b 1
)

REM Build the installer
echo Building installer...
makensis installer.nsi

if errorlevel 1 (
    echo Error: Failed to create installer
    pause
    exit /b 1
)

echo.
echo Installer created successfully!
echo Location: dist\CodePromptOptimizer_Setup.exe
echo.
pause 