@echo off
echo Uninstalling Code Prompt Optimizer...

:: Remove executable from Desktop
del "%USERPROFILE%\Desktop\CodePromptOptimizer.exe"

:: Remove virtual environment
rmdir /s /q venv

:: Remove build directories
rmdir /s /q build
rmdir /s /q dist

echo.
echo Uninstallation complete!
echo Press any key to exit...
pause > nul
