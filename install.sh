#!/bin/bash

echo "Installing Code Prompt Optimizer..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed! Please install Python 3.8 or higher."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed! Please install pip."
    echo "Visit: https://pip.pypa.io/en/stable/installation/"
    exit 1
fi

# Install requirements
echo "Installing required packages..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install requirements!"
    exit 1
fi

# Download NLTK data
echo "Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
if [ $? -ne 0 ]; then
    echo "Failed to download NLTK data!"
    exit 1
fi

# Run setup
echo "Running setup..."
python3 setup.py install
if [ $? -ne 0 ]; then
    echo "Failed to run setup!"
    exit 1
fi

echo
echo "Installation completed successfully!"
echo "To start the application, run: python3 token_script_v2.py"
echo 