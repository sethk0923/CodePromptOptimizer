Code Prompt Optimizer - Python Installation
=======================================

This package contains the Python version of Code Prompt Optimizer, which requires Python to be installed on your system.

System Requirements
-----------------
- Windows 10 or newer
- Python 3.7 or newer
- 500MB free disk space
- Internet connection (for initial setup)

Installation Steps
----------------
1. Make sure Python is installed:
   - Visit python.org/downloads if you need to install Python
   - During Python installation, CHECK "Add Python to PATH"
   
2. Easy Installation:
   - Double-click install.bat
   - Wait for the installation to complete
   - Find CodePromptOptimizer on your Desktop

3. Manual Installation (if install.bat doesn't work):
   a. Open Command Prompt (cmd) as Administrator
   b. Navigate to this folder:
      cd path/to/extracted/folder
   c. Install requirements:
      pip install -r requirements.txt
   d. Run the application:
      python token_script_v2.py

Troubleshooting
--------------
1. "Python not found":
   - Make sure Python is installed
   - Add Python to PATH in System Environment Variables
   - Try restarting your computer

2. "pip not found":
   - Open cmd as Administrator
   - Run: python -m ensurepip --upgrade

3. "Missing dependencies":
   - Open cmd as Administrator
   - Run: pip install --upgrade -r requirements.txt

4. "NLTK data missing":
   - Open Python
   - Run: import nltk; nltk.download('punkt'); nltk.download('stopwords')

Uninstallation
-------------
1. Double-click uninstall.bat
   OR
2. Delete the application from your Desktop

Support
-------
If you encounter any issues:
1. Check the optimizer.log file in the application directory
2. Ensure all prerequisites are installed
3. Try running as Administrator
4. Contact support with the log file attached 