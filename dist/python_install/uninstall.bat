@echo off
echo Uninstalling Code Prompt Optimizer (Python Version)...
echo.

REM Uninstall packages
echo Uninstalling packages...
pip uninstall -y -r requirements.txt

echo.
echo Uninstallation complete!
echo You can now delete this directory.
echo.
pause 