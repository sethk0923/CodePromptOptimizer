#!/bin/bash

set -e  # Exit on error

echo "Installing Code Prompt Optimizer..."
echo

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    echo "Error: Python 3.8 or higher is required."
    echo "Current version: $PYTHON_VERSION"
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv || {
    echo "Failed to create virtual environment!"
    exit 1
}

source venv/bin/activate || {
    echo "Failed to activate virtual environment!"
    exit 1
}

# Upgrade pip and install wheel
echo "Upgrading pip and installing wheel..."
python -m pip install --upgrade pip wheel || {
    echo "Failed to upgrade pip and install wheel!"
    exit 1
}

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt || {
    echo "Failed to install requirements!"
    exit 1
}

# Set up NLTK data directory
echo "Setting up NLTK data directory..."
NLTK_DATA="$HOME/nltk_data"
mkdir -p "$NLTK_DATA"

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')" || {
    echo "Failed to download NLTK data!"
    exit 1
}

# Run setup
echo "Running setup..."
python setup.py install || {
    echo "Failed to run setup!"
    exit 1
}

# Verify installation
echo "Verifying installation..."
if python -c "import tkinter, tiktoken, nltk, requests"; then
    echo "All core packages verified successfully!"
else
    echo "Warning: Some packages may not be installed correctly."
    echo "Please check the error messages above."
fi

echo
echo "Installation completed!"
echo "To start the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python token_script_v2.py"
echo

# Add activation to shell rc file
RC_FILE="$HOME/.$(basename $SHELL)rc"
if [[ -f "$RC_FILE" ]]; then
    echo "# Code Prompt Optimizer virtual environment" >> "$RC_FILE"
    echo "alias cpo-activate='source $(pwd)/venv/bin/activate'" >> "$RC_FILE"
    echo "Added 'cpo-activate' alias to $RC_FILE"
    echo "You can activate the environment by typing: cpo-activate"
fi 