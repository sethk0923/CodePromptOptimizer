@echo off
echo ===== Code Prompt Optimizer v3.0 =====
echo.

rem Check if we need to copy the icon
set ICON_SOURCE=C:\Users\sethk\OneDrive\Documents\tokenizerv2-github\icon.ico
if exist "%ICON_SOURCE%" (
    if not exist "icon.ico" (
        echo Copying icon file...
        copy "%ICON_SOURCE%" "icon.ico" > nul
    )
)

rem Check if we have a compiled executable
if exist "dist\CodePromptOptimizer_v3.exe" (
    rem Copy icon to dist directory if needed
    if exist "%ICON_SOURCE%" (
        if not exist "dist\icon.ico" (
            echo Copying icon to dist directory...
            copy "%ICON_SOURCE%" "dist\icon.ico" > nul
        )
    )
    echo Running compiled executable...
    start "" "dist\CodePromptOptimizer_v3.exe"
    goto end
)

rem Check if Python is available and requirements are installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    goto error
)

rem Check if requirements are installed
if not exist requirements.txt (
    echo Warning: requirements.txt not found. Dependencies may be missing.
) else (
    echo Checking requirements...
    pip list > pip_list.tmp
    findstr /c:"tiktoken" pip_list.tmp > nul
    if %errorlevel% neq 0 (
        echo Installing dependencies...
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            echo Error installing dependencies. Please run:
            echo pip install -r requirements.txt
            goto error
        )
    )
    del pip_list.tmp
)

rem Run the Python script
echo Running Python script...
python token_script_v3.py
goto end

:error
echo.
echo Error: Could not start the application.
echo Press any key to exit.
pause > nul

:end
echo. 