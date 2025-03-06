@echo off
echo ===== Code Prompt Optimizer v3 =====
echo Starting Code Prompt Optimizer v3...

REM Check if icon needs to be copied
python copy_icon.py

REM Run the executable if it exists, otherwise run the Python script
if exist "dist\CodePromptOptimizer_v3.exe" (
    echo Running executable version...
    start "" "dist\CodePromptOptimizer_v3.exe"
) else (
    echo Executable not found, running Python script...
    python token_script_v3.py
)

echo Application started! 