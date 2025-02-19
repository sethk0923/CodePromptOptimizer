from setuptools import setup, find_packages
import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def download_nltk_data():
    """Download required NLTK data."""
    import nltk
    nltk_data = ['punkt', 'stopwords']
    for data in nltk_data:
        nltk.download(data)

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
        ],
        python_requires='>=3.8',
        author="Your Name",
        description="A tool for optimizing code prompts and tokenization",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
    )

if __name__ == "__main__":
    # Install requirements
    print("Installing required packages...")
    install_requirements()
    
    # Download NLTK data
    print("Downloading NLTK data...")
    download_nltk_data()
    
    # Run setup
    main() 