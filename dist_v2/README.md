# Code Prompt Optimizer v2

A powerful tool for optimizing code prompts and managing token limits for large language model interactions.

## Quick Start

1. Double-click `Run_OptimizerV2.bat` to launch the application
2. Type or paste your prompt in the top text box
3. (Optional) Browse for a code file to analyze
4. Click "Optimize Steps" to process your input
5. View the results in the bottom text box
6. Use "Copy to Clipboard" or "Export to TXT" for the results

## Key Features

- **Token Management**: Uses OpenAI's tiktoken for precise token counting
- **Multi-Language Support**: Processes Python, JavaScript, Java, C/C++, HTML, CSS, and plain text
- **Keyword-Based Relevance**: Identifies important keywords in prompts and focuses on relevant code sections
- **Binary File Analysis**: Extracts meaningful information from binary files (PE/EXE)
- **Theme Switching**: Toggle between light and dark themes with a dedicated button
- **Export to Text**: Save analysis results to text files for easy sharing
- **Advanced Code Parsing**: Uses language-specific parsers for accurate code extraction
- **Ghidra Integration**: Optional decompilation of binary files (requires Ghidra setup)

## Files Included

- `CodePromptOptimizerv2.exe` - Main application executable
- `Run_OptimizerV2.bat` - Batch file to launch the application
- `QUICK_START.txt` - Detailed usage instructions
- `GHIDRA_INTEGRATION.txt` - Instructions for setting up Ghidra (optional)
- `icon.ico` - Application icon

## Ghidra Integration (Optional)

For advanced binary analysis features, install Ghidra following the instructions in GHIDRA_INTEGRATION.txt.

## License

This tool is provided under the MIT License.
