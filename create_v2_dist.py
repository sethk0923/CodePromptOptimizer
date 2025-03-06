"""
Create a distribution folder with the renamed executable and updated files.
This script:
1. Creates a new folder called 'dist_v2'
2. Copies necessary files from 'dist' to 'dist_v2'
3. Renames the executable from CodePromptOptimizer_v3.exe to CodePromptOptimizerv2.exe
4. Creates a new batch file to run the renamed executable
"""

import os
import shutil
from pathlib import Path
import sys

# Configure paths
current_dir = Path(os.getcwd())
dist_dir = current_dir / 'dist'
new_dist_dir = current_dir / 'dist_v2'

def create_distribution():
    print("Creating v2 distribution folder...")
    
    # Create the new distribution directory if it doesn't exist
    if not new_dist_dir.exists():
        new_dist_dir.mkdir(parents=True)
        print(f"Created directory: {new_dist_dir}")
    else:
        print(f"Directory already exists: {new_dist_dir}")
    
    # Check if source executable exists
    source_exe = dist_dir / 'CodePromptOptimizer_v3.exe'
    if not source_exe.exists():
        print(f"ERROR: Source executable not found: {source_exe}")
        sys.exit(1)
    
    # Copy and rename the executable
    target_exe = new_dist_dir / 'CodePromptOptimizerv2.exe'
    if not target_exe.exists():
        print(f"Copying and renaming executable to: {target_exe}")
        shutil.copy2(source_exe, target_exe)
    else:
        print(f"Target executable already exists: {target_exe}")
    
    # Copy icon file if it exists
    icon_file = dist_dir / 'icon.ico'
    if icon_file.exists():
        print(f"Copying icon file...")
        shutil.copy2(icon_file, new_dist_dir / 'icon.ico')
    
    # Create updated GHIDRA_INTEGRATION.txt instead of copying
    create_ghidra_integration_file()
    
    # Create a new batch file to run the renamed executable
    create_run_batch_file()
    
    # Create updated quick start guide
    create_quick_start_guide()
    
    # Create a README file
    create_readme_file()
    
    print("\nDistribution folder created successfully!")
    print(f"You can find the renamed executable and related files in: {new_dist_dir}")

def create_run_batch_file():
    """Create a new batch file to run the renamed executable"""
    batch_content = """@echo off
echo ===== Code Prompt Optimizer v2 =====
echo Starting Code Prompt Optimizer v2...

REM Check if icon exists
if not exist "icon.ico" (
    echo Icon file not found, but continuing...
)

echo Running executable...
start "" "CodePromptOptimizerv2.exe"

echo Application started!
"""
    
    batch_file = new_dist_dir / 'Run_OptimizerV2.bat'
    with open(batch_file, 'w') as f:
        f.write(batch_content)
    
    print(f"Created batch file: {batch_file}")

def create_quick_start_guide():
    """Create an updated quick start guide"""
    quick_start_content = """Code Prompt Optimizer v2.0 - Quick Start Guide
=====================================

Getting Started
--------------
1. Double-click 'Run_OptimizerV2.bat' to launch the application
2. The modern interface will open with dark theme by default (light theme also available)

Basic Usage
----------
1. Type or paste your prompt into the top text box
   - Use Tab key for predictive text suggestions
   - Watch the real-time token counter as you type
   - Keywords from your prompt will be used to find relevant code sections
2. (Optional) Click "Browse" to include a code or binary file
3. Click "Optimize Steps" to process your input
4. View the optimized output in the bottom text box
   - Notice relevance scores next to each code section (higher is better)
   - Sections are sorted by relevance to your prompt keywords
5. Click "Copy to Clipboard" to copy the results
6. Click "Export to TXT" to save results as a text file

Supported File Types
------------------
- Python (.py)
- JavaScript (.js)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- HTML (.html, .htm)
- CSS (.css)
- Binary (.exe, .dll, .so, .dylib, .elf)
- Text (.txt)

Feature Highlights
------------------
- Modern graphite window bar for sleek look
- Light and dark theme switching with dedicated button
- Keyword extraction for more relevant code section identification
- Export to text file functionality
- Tab-based predictive text
- Real-time token counting
- More accurate tokenization with tiktoken
- Advanced code parsing for all languages
- Binary file analysis with Ghidra integration (optional)
- Clipboard integration
- Responsive threaded processing

Understanding Relevance Scores
----------------------------
- When you enter a prompt, the optimizer extracts important keywords
- Each code section is analyzed for these keywords
- Sections are assigned a relevance score from 0-100
- Higher scores indicate better matches to your prompt keywords
- Sections are sorted by relevance score in the output
- The status bar shows which keywords were matched

Token Limits
-----------
- Maximum total tokens: 2,500
- Maximum tokens per step: 500

Need Help?
---------
- Missing libraries? Run 'pip install -r requirements.txt'
- For Ghidra setup, see GHIDRA_INTEGRATION.txt

Note: This is a standalone executable - no installation required!
"""
    
    quick_start_file = new_dist_dir / 'QUICK_START.txt'
    with open(quick_start_file, 'w') as f:
        f.write(quick_start_content)
    
    print(f"Created updated quick start guide: {quick_start_file}")

def create_readme_file():
    """Create a README file for the v2 distribution"""
    readme_content = """# Code Prompt Optimizer v2

A powerful tool for optimizing code prompts and managing token limits for large language model interactions.

## Quick Start

1. Double-click `Run_OptimizerV2.bat` to launch the application
2. Type or paste your prompt in the top text box
3. (Optional) Browse for a code file to analyze
4. Click "Optimize Steps" to process your input
5. View the results in the bottom text box
6. Use "Copy to Clipboard" or "Export to TXT" for the results

## Key Features

- **Token Management**: Uses OpenAI's tiktoken for precise token counting
- **Multi-Language Support**: Processes Python, JavaScript, Java, C/C++, HTML, CSS, and plain text
- **Keyword-Based Relevance**: Identifies important keywords in prompts and focuses on relevant code sections
- **Binary File Analysis**: Extracts meaningful information from binary files (PE/EXE)
- **Theme Switching**: Toggle between light and dark themes with a dedicated button
- **Export to Text**: Save analysis results to text files for easy sharing
- **Advanced Code Parsing**: Uses language-specific parsers for accurate code extraction
- **Ghidra Integration**: Optional decompilation of binary files (requires Ghidra setup)

## Files Included

- `CodePromptOptimizerv2.exe` - Main application executable
- `Run_OptimizerV2.bat` - Batch file to launch the application
- `QUICK_START.txt` - Detailed usage instructions
- `GHIDRA_INTEGRATION.txt` - Instructions for setting up Ghidra (optional)
- `icon.ico` - Application icon

## Ghidra Integration (Optional)

For advanced binary analysis features, install Ghidra following the instructions in GHIDRA_INTEGRATION.txt.

## License

This tool is provided under the MIT License.
"""
    
    readme_file = new_dist_dir / 'README.md'
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    print(f"Created README file: {readme_file}")

def create_ghidra_integration_file():
    """Create an updated GHIDRA_INTEGRATION.txt file with references to the new executable name"""
    ghidra_content = """# Ghidra Integration for Code Prompt Optimizer v2

This document provides detailed instructions for setting up and using the Ghidra integration in the Code Prompt Optimizer v2.

## What is Ghidra?

Ghidra is a software reverse engineering (SRE) framework developed by the National Security Agency (NSA). It provides powerful binary analysis capabilities including disassembly, decompilation, and more. The Code Prompt Optimizer uses Ghidra's headless analyzer to provide enhanced insights into binary files.

## Installation

1. Download Ghidra from the official website: https://ghidra-sre.org/
2. Install Ghidra by extracting the archive to a permanent location.
   - Recommended locations:
     - Windows: `C:\\Program Files\\Ghidra` or `C:\\Ghidra`
     - Linux: `/opt/ghidra` or `/usr/local/ghidra`
     - macOS: `/Applications/Ghidra` or `~/ghidra`

## Configuration

There are two ways to configure the Code Prompt Optimizer to find your Ghidra installation:

### Method 1: Add Ghidra to your PATH (Recommended)

1. Locate the `analyzeHeadless` script in your Ghidra installation:
   - Windows: `<Ghidra Installation>\\support\\analyzeHeadless.bat`
   - Linux/macOS: `<Ghidra Installation>/support/analyzeHeadless`

2. Add the directory containing this script to your system PATH:
   - Windows:
     - Open System Properties > Advanced > Environment Variables
     - Edit the PATH variable and add the full path to Ghidra's support directory
     - Example: `C:\\Program Files\\Ghidra\\support`

   - Linux/macOS:
     - Add to ~/.bashrc or ~/.zshrc: `export PATH="$PATH:/path/to/ghidra/support"`
     - Apply with: `source ~/.bashrc` or restart your terminal

### Method 2: Set the GHIDRA_HOME Environment Variable

1. Set the GHIDRA_HOME environment variable to point to your Ghidra installation directory:
   - Windows:
     - Open System Properties > Advanced > Environment Variables
     - Create a new variable GHIDRA_HOME with the value of your Ghidra installation path
     - Example: `C:\\Program Files\\Ghidra`

   - Linux/macOS:
     - Add to ~/.bashrc or ~/.zshrc: `export GHIDRA_HOME="/path/to/ghidra"`
     - Apply with: `source ~/.bashrc` or restart your terminal

## Usage

Once configured, the Code Prompt Optimizer will automatically detect Ghidra and use it for binary analysis:

1. Launch the Code Prompt Optimizer by running Run_OptimizerV2.bat
2. Enter your prompt in the text area
3. Use the file browser to select a binary file (.exe, .dll, .so, etc.)
4. Click "Analyze"
5. The application will detect it's a binary file and use Ghidra for analysis
6. Status messages will indicate when Ghidra is being used
7. Analysis results will include decompiled code when possible

## Notes

- Ghidra analysis can take 1-2 minutes for the first run on a binary file
- Subsequent analyses of the same file will be faster
- The analyzer creates temporary project files that are deleted after analysis
- Binary analysis without Ghidra is still available but provides less detail
- If analysis fails, the application will fall back to basic binary inspection

## Troubleshooting

If the Code Prompt Optimizer cannot find Ghidra:

1. Verify that Ghidra is installed correctly
2. Check that the analyzeHeadless script exists in the support directory
3. Ensure your PATH or GHIDRA_HOME environment variable is set correctly
4. Restart the application after making any configuration changes
5. Check the application console for error messages

For further assistance, consult the Ghidra documentation at https://ghidra-sre.org/
"""
    
    ghidra_file = new_dist_dir / 'GHIDRA_INTEGRATION.txt'
    with open(ghidra_file, 'w') as f:
        f.write(ghidra_content)
    
    print(f"Created updated GHIDRA_INTEGRATION.txt file: {ghidra_file}")

if __name__ == "__main__":
    create_distribution() 