# Code Prompt Optimizer

A powerful tool for optimizing code prompts and managing token limits for large language model interactions.

## Features

- **Token Management**: Automatically splits large prompts into manageable chunks within token limits
- **Code Block Handling**: Intelligently processes code blocks from various programming languages
- **Support for Multiple Languages**: Handles Python, JavaScript, HTML, CSS, and plain text files
- **Token Counting**: Real-time token counting for prompt optimization
- **GUI Interface**: User-friendly graphical interface for easy interaction
- **NLTK Integration**: Advanced text processing capabilities

## Installation

### Option 1: Running the Executable (Windows)

1. Download `CodePromptOptimizer.exe` from the `dist` directory
2. Double-click the executable to run the application
3. No additional installation or dependencies required

### Option 2: Running from Source

1. Ensure Python 3.9+ is installed
2. Install required packages:
   ```bash
   pip install tiktoken==0.9.0 nltk transformers
   ```
3. Run the script:
   ```bash
   python token_script_v2.py
   ```

## Usage

1. **Launch the Application**
   - Run `CodePromptOptimizer_v2.exe` or execute `token_script_v2.py`
   - A window will appear with the GUI interface

2. **Enter Your Prompt**
   - Type or paste your prompt text in the upper text box
   - The prompt can include natural language and code snippets

3. **Optional: Include Code Files**
   - Click "Browse" to select a code file
   - Supported file types: .py, .js, .html, .css, .txt
   - The tool will automatically extract relevant code blocks

4. **Generate Optimized Steps**
   - Click "Optimize Steps" to process your input
   - The tool will split the content into token-optimized chunks
   - Each chunk will be displayed with its token count

## Token Limits

- Maximum total tokens: 2500
- Maximum tokens per step: 500
- The tool automatically manages these limits

## Code Block Processing

The optimizer handles different file types with specialized processing:
- **Python**: Functions and classes
- **JavaScript**: Functions and classes
- **HTML**: Script tags, style tags, and HTML elements
- **CSS**: Rules, media queries, and keyframes
- **Text**: Line-by-line processing

## Troubleshooting

1. **GUI Not Appearing**
   - Ensure no other instances are running
   - Check for sufficient system resources

2. **File Processing Issues**
   - Verify file permissions
   - Ensure file is in a supported format
   - Check file encoding (UTF-8 recommended)

3. **Token Counting Discrepancies**
   - Different tokenizers may produce slightly different results
   - The tool uses a basic word-splitting approach for estimation

## Technical Details

- Built with Python 3.9
- Uses Tkinter for GUI
- NLTK for text processing
- Regular expressions for code block extraction
- Token counting based on word splitting

## License

This tool is provided as-is for personal and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your input meets the format requirements
3. Ensure all dependencies are correctly installed

## Version History

- v2.0: Added NLTK integration, improved code block handling
- v1.0: Initial release with basic token management