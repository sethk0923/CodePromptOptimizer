# Code Prompt Optimizer

A powerful tool for optimizing code prompts and managing token limits for large language model interactions, with enhanced support for multiple programming languages and binary files.

## Features

- **Accurate Token Management**: Uses OpenAI's `tiktoken` for precise token counting
- **Multi-Language Support**: Processes Python, JavaScript, Java, C/C++, HTML, CSS, and plain text
- **Keyword-Based Relevance**: Identifies important keywords in prompts and focuses on relevant code sections
- **Light/Dark Themes**: Toggle between light and dark themes with a dedicated button
- **Binary File Analysis**: Extracts meaningful information from binary files (PE/EXE)
- **Export to Text**: Save analysis results to text files for easy sharing
- **Advanced Code Parsing**: Uses language-specific parsers for accurate code extraction
- **Ghidra Integration**: Optional decompilation of binary files with NSA's Ghidra reverse engineering tool
- **Modern GUI Interface**: Graphite window bar and responsive interface with predictive text
- **Real-time Token Counting**: See token counts as you type
- **Copy to Clipboard**: Easily copy optimized output
- **Enhanced Tokenization**: Splits large prompts into manageable chunks
- **Code Formatting**: Applies formatting standards when possible
- **Threaded Processing**: Responsive UI even during heavy processing

## What's New in Version 3

- **Theme Switching**: Toggle between light and dark themes with a single click
- **Graphite Window Bar**: Modern window styling with customized title bar
- **Keyword Extraction**: Identifies key terms in your prompt to find relevant code
- **Relevance Scoring**: Shows how well each code section matches your keywords
- **Export Functionality**: Save results directly to text files
- **Enhanced UI**: Better status feedback and progress indicators

## Installation

### Option 1: Running the Executable (Windows)

1. Download the latest executable from the `dist` directory
2. Double-click `Run_Optimizer_v3.bat` to run the application 
3. No additional installation or dependencies required

### Option 2: Running from Source

1. Ensure Python 3.9+ is installed
2. Clone this repository
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   This will install all required dependencies including: tiktoken, nltk, tree-sitter, and more
4. Download NLTK data (if not automatically downloaded):
   ```bash
   python -c "import nltk; nltk.download('words')"
   ```
5. Run the script:
   ```bash
   python token_script_v3.py
   ```

### Option 3: Ghidra Integration (Optional)

For advanced binary decompilation features:

1. Download and install Ghidra from [https://ghidra-sre.org/](https://ghidra-sre.org/)
2. Install it in a standard location:
   - Windows: `C:\Program Files\Ghidra` or `C:\Ghidra`
   - Linux/macOS: `/opt/ghidra`, `/usr/local/ghidra`, or `~/ghidra`
   
   OR
   
3. Set the `GHIDRA_HOME` environment variable to your Ghidra installation directory

The application will automatically detect Ghidra and use it for binary analysis when available.

## Usage

1. **Launch the Application**
   - Run the executable or execute `token_script_v3.py`
   - The modern dark-themed interface will appear

2. **Enter Your Prompt**
   - Type or paste your prompt text in the upper text box
   - Use Tab key for predictive text suggestions
   - Watch the real-time token counter

3. **Include Code Files (Optional)**
   - Click "Browse" to select a code or binary file
   - Supported file types now include:
     - Python (.py)
     - JavaScript (.js)
     - Java (.java)
     - C/C++ (.c, .cpp, .h, .hpp)
     - HTML (.html, .htm)
     - CSS (.css)
     - Text (.txt)
     - Binary (.exe, .dll)

4. **Generate Optimized Steps**
   - Click "Optimize Steps" to process your input
   - The tool will split the content into token-optimized chunks
   - Each chunk will be displayed with its token count

5. **Copy Results**
   - Click "Copy to Clipboard" to copy the optimized output

## Token Limits

- Maximum total tokens: 2500
- Maximum tokens per step: 500
- The tool automatically manages these limits using accurate tokenization

## Code Block Processing

The optimizer now uses specialized parsers for different file types:
- **Python**: AST parser for accurate function and class extraction
- **JavaScript**: Esprima for parsing JS structures
- **HTML**: BeautifulSoup for extracting elements
- **Java**: Javalang parser for methods and classes
- **C/C++**: Tree-sitter and PyCParser for accurate parsing
- **Binary**: 
  - **Ghidra**: Advanced decompilation into C-like source code (when available)
  - **pefile/pyelftools**: PE/ELF metadata extraction
  - **Fallback**: Basic binary information extraction

## Advanced Features

- **Tree-sitter Integration**: Language-agnostic parsing capabilities
- **Ghidra Integration**: Deep binary analysis and decompilation to C-like code
- **Predictive Text**: Tab-based autocomplete with programming keywords
- **Real-time Token Counting**: See token counts as you type
- **Clipboard Integration**: Copy results with one click
- **Dark Theme**: Modern, eye-friendly interface

## Troubleshooting

1. **Missing Libraries**
   - If you see import errors, run `pip install -r requirements.txt`
   - Some binary analysis libraries are optional

2. **NLTK Data Not Downloaded**
   - The app will attempt to download required NLTK data automatically
   - If this fails, run `python -c "import nltk; nltk.download('words')"`

3. **Tree-sitter Grammars**
   - If you're compiling from source and want to use Tree-sitter, you'll need language grammars
   - Create a directory `tree-sitter-grammars` and add compiled language `.so` files

4. **Ghidra Integration**
   - If Ghidra isn't detected automatically, set the `GHIDRA_HOME` environment variable
   - Binary decompilation can take 1-2 minutes per file
   - If you encounter issues, ensure you're using Ghidra 10.0 or newer

5. **File Processing Issues**
   - The application now has better encoding detection
   - For binary files, only limited information can be extracted without Ghidra

## Technical Details

- Built with Python 3.9+
- Uses Tkinter/ttk for the modern GUI
- OpenAI's tiktoken for accurate token counting
- Tree-sitter and language-specific parsers
- Ghidra integration for advanced binary analysis
- Multithreading for responsive UI
- Compiled with PyInstaller for standalone executables

## License

This tool is provided under the MIT License.

## Version History

- v3.0: Complete rewrite with advanced parsing, binary support, modern GUI
- v2.0: Added NLTK integration, improved code block handling
- v1.0: Initial release with basic token management