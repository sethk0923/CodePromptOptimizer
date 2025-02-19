# Code Prompt Optimizer

A simple tool with a window (GUI) to help you make prompts and code files shorter and easier for AI tools like chatbots. It cuts down extra words and splits everything into small steps you can copy and paste one by one.

## Features
- **Prompt Shortening**: Takes your prompt (what you want to ask an AI) and makes it shorter without losing its meaning.
- **Code File Help**: Reads code files (like `.py` or `.js`) and pulls out important parts (like functions) to use as steps.
- **Step-by-Step**: Breaks your prompt and code into small pieces (up to 500 tokens each), with a total limit of 130,000 tokens.
- **Easy to Use**: Works on Windows and macOS with a clickable icon—no tricky setup needed.

## Download and Installation

### Quick Download
Visit our [Releases page](https://github.com/sethk0923/CodePromptOptimizer/releases) to download:
- **Windows Installer**: Download `CodePromptOptimizer_Setup.exe` for a proper Windows installation
- **Windows Standalone**: Download `CodePromptOptimizer_Standalone.zip` for a portable version
- **Python Package**: Download `CodePromptOptimizer_Python.zip` if you prefer running with Python

### Installation Options

#### Option 1: Windows Installer (Recommended)
1. Download `CodePromptOptimizer_Setup.exe` from the [Releases page](https://github.com/sethk0923/CodePromptOptimizer/releases)
2. Run the installer
3. Follow the installation wizard
4. Find the application in:
   - Start Menu
   - Desktop shortcut
   - Programs and Features

#### Option 2: Standalone Installation (Windows)
1. Download `CodePromptOptimizer_Standalone.zip`
2. Extract the ZIP file
3. Run `CodePromptOptimizer.exe`
   - No installation required
   - Portable version

#### Option 3: Python Installation (All Platforms)
1. Download `CodePromptOptimizer_Python.zip`
2. Make sure you have Python 3.7+ installed
3. Extract the ZIP file
4. Open a terminal in the extracted folder
5. Run: `pip install -r requirements.txt`
6. Start the app: `python token_script_v2.py`

## Development Setup

If you want to contribute or modify the code:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sethk0923/CodePromptOptimizer.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Development Version**:
   ```bash
   python token_script_v2.py
   ```

## Prerequisites
- **Python 3.7 or Newer**: A free program you need on your computer to run this tool (we'll help you get it).
- **Extra Tools**: Some small add-ons (listed in `requirements.txt`) that we'll install for you.

## Git LFS
This repository uses Git Large File Storage (Git LFS) to handle large files. To clone and use this repository:

1. **Install Git LFS**:
   - Download from [git-lfs.github.com](https://git-lfs.github.com/)
   - Or use package managers:
     ```bash
     # Windows (with Chocolatey)
     choco install git-lfs

     # macOS (with Homebrew)
     brew install git-lfs
     ```

2. **Clone the Repository**:
   ```bash
   # Initialize Git LFS
   git lfs install

   # Clone the repository
   git clone https://github.com/sethk0923/CodePromptOptimizer.git
   ```

3. **Alternative Download**:
   If you don't want to use Git LFS, you can download the release packages directly from the [Releases page](https://github.com/sethk0923/CodePromptOptimizer/releases).

## Usage

### Opening the Tool
- **With Python**: After Step 3 above, the window opens.
- **With Icon**: Double-click the `.exe` or `.app` file on your Desktop.

### Using the Window
1. **Type Your Question**:
   - In the "Enter Your Prompt" box, write what you want to ask an AI, like "Check this code for mistakes."
2. **Pick a Code File (If You Want)**:
   - Click "Browse" next to "Select Code File," find your code file (e.g., `mycode.py`), and click "Open." You can skip this if you just have a question.
3. **Make Steps**:
   - Click the "Optimize Steps" button. Wait a second, and you'll see steps in the big box below.
4. **Copy to Your AI**:
   - Look at the steps in the box. Copy each one (e.g., click and drag over "Step 1," right-click, "Copy"), then paste it into your AI chatbot or tool one at a time.

## Examples

### Example 1: Just a Question
- **What You Type**: "Write a detailed guide on training a dog to sit and stay with lots of examples"
- **Steps You Get**:
  ```
  Step 1 (Tokens: 8):
  write guide training dog sit

  Step 2 (Tokens: 6):
  stay examples
  ```
- **How to Use**:
  1. Open your AI tool (like ChatGPT or a composer).
  2. Copy "Step 1" and paste it in. Press Enter or "Send."
  3. After it answers, copy "Step 2" and paste it next. Send again.

### Example 2: Question with a Small Code File
- **What You Type**: "Review this Python script for errors and suggest improvements"
- **File (script.py)**:
  ```python
  def calculate_sum(a, b):
      # Adds two numbers
      return a + b

  result = calculate_sum(5, 10)
  print(result)
  ```
- **Steps You Get**:
  ```
  Step 1 (Tokens: 8):
  review python script errors suggest improvements

  Step 2 (Tokens: 11):
  def calculate_sum(a, b): return a + b

  Step 3 (Tokens: 8):
  result = calculate_sum(5, 10) print(result)
  ```
- **How to Use**:
  1. Open your AI chatbot.
  2. Paste "Step 1" and send it.
  3. Paste "Step 2" (the function) and send it after the first answer.
  4. Paste "Step 3" (the rest) and send it last.

### Example 3: Question with a Bigger Code File
- **What You Type**: "Analyze this JavaScript code"
- **File (script.js)**:
  ```javascript
  function greet(name) {
      // Say hello
      console.log("Hello, " + name);
  }
  function add(a, b) {
      return a + b;
  }
  greet("Alice");
  console.log(add(2, 3));
  ```
- **Steps You Get**:
  ```
  Step 1 (Tokens: 3):
  analyze javascript code

  Step 2 (Tokens: 11):
  function greet(name) { console.log("Hello, " + name); }

  Step 3 (Tokens: 9):
  function add(a, b) { return a + b; }

  Step 4 (Tokens: 7):
  greet("Alice"); console.log(add(2, 3));
  ```
- **How to Use**:
  1. Start your AI tool.
  2. Copy "Step 1" (the question), paste it, and send.
  3. Copy "Step 2" (first function), paste it, and send.
  4. Copy "Step 3" (second function), paste it, and send.
  5. Copy "Step 4" (the calls), paste it, and send.

## What to Expect
- **Steps List**: You'll see a list like "Step 1," "Step 2," etc., with a number in parentheses (e.g., Tokens: 8) showing how "big" each step is for the AI. Each step is small (500 or fewer), and all steps together won't go over 130,000.
- **Code Stays Clear**: If you add a code file, the tool keeps the code looking right (like spacing and brackets) so the AI understands it.
- **Shorter Words**: Your question gets cut down (e.g., "lots of examples" becomes "examples"), but it still makes sense.
- **Pop-Up Warning**: If you forget to type a question, a little box will tell you to add one.

## Notes
- **Files It Likes**: Works great with code files like `.py` (Python), `.js` (JavaScript), `.cpp` (C++), `.java` (Java), or `.txt`. Other files (like pictures) might show weird text.
- **Size Limits**: Each step is 500 tokens or less, and everything together stays under 130,000 tokens. A "token" is like a word or piece the AI reads.
- **Changing It**: If you want bigger or smaller steps, ask someone to tweak the numbers in the `code_prompt_optimizer.py` file.

## Troubleshooting
- **Nothing Shows Up**: Did you type a question? If the "Enter Your Prompt" box is empty, it won't work—type something and try again.
- **File Won't Load**: Make sure you picked the right file. If it's not a text or code file, it might not work right. Try a `.txt` or `.py` file instead.
- **Error Messages**: If you see "command not found" or "module missing," you might need to install Python or the helpers again. Go back to "Add the Helpers" in Installation and type the `pip install` line.
- **Window Won't Open**: If you double-click the icon and nothing happens, try running it with Python (Option 1) to see if there's a hint about what's wrong.