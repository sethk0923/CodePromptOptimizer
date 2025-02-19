# Code Prompt Optimizer

A powerful tool for optimizing code prompts and tokenization, with support for multiple programming languages including Python, JavaScript, HTML, CSS, TypeScript, and Java.

## Features

- Multi-language code block recognition
- Intelligent token optimization
- Support for large files and code blocks
- GUI interface for easy interaction
- Automatic token counting and optimization
- Support for HTML, CSS, JavaScript, TypeScript, Python, and Java

## Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Windows, macOS, or Linux operating system

## Installation

### Quick Installation (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/code-prompt-optimizer.git
   cd code-prompt-optimizer
   ```

2. Run the setup script:
   ```bash
   python setup.py install
   ```

This will automatically:
- Install all required packages
- Download necessary NLTK data
- Set up the application

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/code-prompt-optimizer.git
   cd code-prompt-optimizer
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Download NLTK data:
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## Usage

1. Start the application:
   ```bash
   python token_script_v2.py
   ```

2. In the GUI:
   - Enter your prompt in the text area
   - (Optional) Select a code file to analyze
   - Click "Optimize Steps" to process

## Troubleshooting

### Common Issues

1. **Tiktoken Installation Issues**
   ```bash
   pip uninstall tiktoken
   pip install tiktoken==0.8.0
   ```

2. **NLTK Data Missing**
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

3. **GUI Issues**
   - Ensure Tkinter is installed:
     ```bash
     pip install tk
     ```

### Error Logs

Check `optimizer.log` in the application directory for detailed error messages and debugging information.

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.