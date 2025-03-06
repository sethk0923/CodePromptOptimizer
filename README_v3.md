# Code Prompt Optimizer v3

## Overview

The Code Prompt Optimizer is a powerful tool designed to analyze and optimize code snippets for AI-based code generation. Version 3 introduces significant improvements including new libraries, enhanced functionality, modernized GUI, and better binary analysis capabilities.

## Key Features

- **Token Analysis**: Accurately counts tokens using OpenAI's tiktoken library
- **Tree-sitter Integration**: Provides advanced code parsing and syntax highlighting
- **Language Detection**: Automatically identifies the programming language of your code
- **Keyword-Based Relevance**: Identifies important keywords in your prompt and focuses on the most relevant code sections
- **Optimization Suggestions**: Offers context-specific recommendations to improve your code prompts
- **Binary Analysis**: Analyzes binary files using both basic binary inspection and advanced Ghidra decompilation
- **Modern GUI**: Clean, intuitive interface with improved visual elements
- **Theme Switching**: Toggle between light and dark themes with a dedicated button
- **Custom Window Bar**: Enhanced window appearance with graphite-colored title bar
- **Export Options**: Save your results to text files for easy sharing
- **Standalone Executable**: Easy to install and run on Windows systems

## New in Version 3

- Integration with **tiktoken** for accurate OpenAI token counting
- Support for **tree-sitter** for superior code parsing and syntax highlighting
- **Keyword-based relevance** filtering to focus on the most important code sections
- Advanced **Ghidra integration** for sophisticated binary analysis
- **Theme switching** with light and dark mode support
- **Graphite window bar** for a modern look
- **Export to text file** functionality for easier sharing of results
- Improved **GUI layout** with consistent styling and better user experience
- Enhanced **export options** for saving analysis results
- Streamlined **installation process** with better dependency management
- Custom **application icon** for better system integration
- Comprehensive **documentation** for all features

## Requirements

- Python 3.9+ (for running from source)
- Dependencies listed in requirements.txt

## Installation

### Option 1: Run the Executable (Recommended for Windows)

1. Download the latest release
2. Run `Run_Optimizer_v3.bat` to start the application

### Option 2: Run from Source

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python token_script_v3.py`

## Building from Source

To build your own executable:

1. Install PyInstaller: `pip install pyinstaller`
2. Run the build script: `python build_executable.py`
3. The executable will be created in the `dist` directory

## Ghidra Integration

For advanced binary analysis, Ghidra integration is available. To use this feature:

1. Install Ghidra from the [official website](https://ghidra-sre.org/)
2. Ensure Ghidra's `analyzeHeadless` script is in your PATH or set the `GHIDRA_HOME` environment variable
3. See `GHIDRA_INTEGRATION.txt` for more detailed setup instructions

## Usage

1. Launch the application using the executable or from source
2. Paste your code into the input area
3. Enter a prompt that describes what you're looking for (the application will extract keywords from this)
4. Select a file to analyze (optional)
5. Click "Analyze" to process the code
6. Toggle between light and dark themes using the theme button
7. Export your results to a text file using the export button
8. View token counts, language detection, and optimization suggestions
9. Note the relevance scores that show how well each section matches your prompt keywords

## File Descriptions

- `token_script_v3.py`: Main application file
- `build_executable.py`: Script to build the standalone executable
- `copy_icon.py`: Utility to ensure the application icon is available
- `Run_Optimizer_v3.bat`: Batch file to easily run the application
- `requirements.txt`: List of Python dependencies
- `GHIDRA_INTEGRATION.txt`: Instructions for setting up Ghidra

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the tiktoken library
- Tree-sitter project for advanced code parsing
- NSA for the Ghidra decompiler
- All contributors and users who have provided feedback and suggestions 