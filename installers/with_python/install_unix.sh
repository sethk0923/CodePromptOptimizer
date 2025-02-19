#!/bin/bash

set -e  # Exit on error

echo "Installing Code Prompt Optimizer (Python Version)..."
echo

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    echo "Error: Python 3.8 or higher is required."
    echo "Current version: $PYTHON_VERSION"
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Install requirements
echo "Installing required packages..."
pip3 install -r requirements.txt || {
    echo "Failed to install requirements!"
    exit 1
}

# Set up NLTK data directory
echo "Setting up NLTK data directory..."
NLTK_DATA="$HOME/nltk_data"
mkdir -p "$NLTK_DATA"

# Download NLTK data
echo "Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')" || {
    echo "Failed to download NLTK data!"
    exit 1
}

# Verify installation
echo "Verifying installation..."
if python3 -c "import tkinter, tiktoken, nltk, requests"; then
    echo "All core packages verified successfully!"
else
    echo "Warning: Some packages may not be installed correctly."
    echo "Please check the error messages above."
fi

echo
echo "Installation completed!"
 