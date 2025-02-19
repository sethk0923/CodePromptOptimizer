# Code Prompt Optimizer v1.0.0

First release of Code Prompt Optimizer - a GUI tool that helps optimize prompts and code files for AI tools.

## Download Options

Choose the package that best suits your needs:

### 1. Windows Standalone Package (`CodePromptOptimizer_Standalone_20250218.zip`)
- No Python installation required
- Just extract and run
- Best for most Windows users

### 2. Python Package (`CodePromptOptimizer_Python_20250218.zip`)
- Requires Python 3.7+
- Works on Windows, macOS, and Linux
- Best for developers or users who prefer Python

## Installation Instructions

### Windows Standalone Installation
1. Download `CodePromptOptimizer_Standalone_20250218.zip`
2. Right-click the ZIP file and select "Extract All..."
3. Choose a destination folder (e.g., Desktop)
4. Open the extracted folder
5. Double-click `CodePromptOptimizer.exe` to run
   - If Windows SmartScreen appears, click "More info" then "Run anyway"

### Python Installation (All Platforms)
1. Download `CodePromptOptimizer_Python_20250218.zip`
2. Make sure Python 3.7 or newer is installed
   - Download from [python.org](https://www.python.org/downloads/) if needed
   - Check "Add Python to PATH" during installation
3. Extract the ZIP file
4. Open a terminal/command prompt in the extracted folder
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the application:
   ```bash
   python token_script_v2.py
   ```

## Features
- Optimize prompts by removing unnecessary words while preserving meaning
- Parse code files and extract relevant functions/classes
- Split content into manageable chunks (max 500 tokens each)
- Track token count for each step
- User-friendly GUI interface
- Support for multiple programming languages

## System Requirements

### Standalone Version
- Windows 10 or newer
- 500MB free disk space
- 4GB RAM recommended

### Python Version
- Python 3.7 or newer
- 500MB free disk space
- Supported platforms:
  - Windows 10+
  - macOS 10.14+
  - Linux (most modern distributions)

## Troubleshooting

### Common Issues

1. "Windows protected your PC" message
   - Click "More info"
   - Select "Run anyway"
   - This appears because we're a new publisher

2. Missing Python (Python version only)
   - Download Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
   - Restart your computer after installation

3. Application won't start
   - Try running as Administrator
   - Check Windows Defender/Antivirus settings
   - Ensure all files were extracted from the ZIP

4. "Module not found" error (Python version)
   - Open terminal/command prompt
   - Navigate to the application folder
   - Run: `pip install -r requirements.txt`

For additional help, please open an issue on GitHub. 