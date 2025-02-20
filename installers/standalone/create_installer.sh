#!/bin/bash

set -e  # Exit on error

echo "Creating standalone installer for Code Prompt Optimizer..."
echo

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    echo "Error: Python 3.8 or higher is required to create the installer."
    echo "Current version: $PYTHON_VERSION"
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" &>/dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller || {
        echo "Failed to install PyInstaller!"
        exit 1
    }
fi

# Create the installer
echo "Creating installer..."
python3 create_installers.py --icon=../../assets/icon.ico || {
    echo "Failed to create installer!"
    exit 1
}

echo
echo "Installer creation completed!"
echo "Check the macos/output directory for the installer."
echo

# Make the installer executable
if [ -f "macos/output/CodePromptOptimizer.app" ]; then
    chmod +x "macos/output/CodePromptOptimizer.app/Contents/MacOS/CodePromptOptimizer"
fi
