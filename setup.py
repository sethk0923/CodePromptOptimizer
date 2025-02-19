from setuptools import setup, find_packages
import subprocess
import sys
import os
import platform

def install_requirements():
    """Install required packages."""
    # Upgrade pip first
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    # Install wheel for better package management
    subprocess.check_call([sys.executable, "-m", "pip", "install", "wheel"])
    # Install requirements
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def download_nltk_data():
    """Download required NLTK data."""
    import nltk
    nltk_data = ['punkt', 'stopwords', 'averaged_perceptron_tagger']
    for data in nltk_data:
        nltk.download(data)

def verify_installation():
    """Verify that all components are installed correctly."""
    try:
        import tkinter
        import tiktoken
        import nltk
        import requests
        print("All core packages verified successfully!")
        return True
    except ImportError as e:
        print(f"Error: Failed to import {str(e).split()[-1]}")
        return False

def setup_nltk_data_path():
    """Set up NLTK data path in user's home directory."""
    import nltk
    nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
    os.makedirs(nltk_data_path, exist_ok=True)
    nltk.data.path.append(nltk_data_path)

def main():
    setup(
        name="code-prompt-optimizer",
        version="1.0.0",
        packages=find_packages(),
        install_requires=[
            'tiktoken==0.8.0',
            'nltk==3.8.1',
            'requests==2.31.0',
            'tk==0.1.0',
            'setuptools>=65.5.1',
            'wheel>=0.40.0',
            'python-dotenv==1.0.0',
            'pathlib==1.0.1',
            'typing-extensions>=4.7.1',
            'pillow>=10.0.0',
            'certifi>=2023.7.22',
            'charset-normalizer>=3.2.0',
            'idna>=3.4',
            'urllib3>=2.0.4',
            'packaging>=23.1',
        ],
        python_requires='>=3.8',
        author="Your Name",
        description="A tool for optimizing code prompts and tokenization",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        classifiers=[
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Text Processing :: Linguistic",
        ],
        entry_points={
            'console_scripts': [
                'code-prompt-optimizer=token_script_v2:main',
            ],
        },
    )

if __name__ == "__main__":
    print("Starting installation...")
    
    # Set up NLTK data path
    print("Setting up NLTK data path...")
    setup_nltk_data_path()
    
    # Install requirements
    print("Installing required packages...")
    install_requirements()
    
    # Download NLTK data
    print("Downloading NLTK data...")
    download_nltk_data()
    
    # Run setup
    print("Running setup...")
    main()
    
    # Verify installation
    print("Verifying installation...")
    if verify_installation():
        print("\nInstallation completed successfully!")
        print("To start the application, run: python token_script_v2.py")
    else:
        print("\nInstallation completed with warnings. Please check the error messages above.") 