import os
import subprocess
import shutil

def clean_build_dirs():
    """Clean up build and dist directories"""
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def build_executable():
    """Build the executable using PyInstaller"""
    # Clean up first
    clean_build_dirs()
    
    # Build command
    cmd = [
        'pyinstaller',
        '--clean',
        '--name=CodePromptOptimizer',
        '--onefile',
        '--noconsole',
        '--add-data', f'icon.ico{os.pathsep}.',
        '--add-data', f'LICENSE{os.pathsep}.',
        'token_script_v2.py'
    ]
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output
    print("=== Build Output ===")
    print(result.stdout)
    
    if result.stderr:
        print("=== Build Errors ===")
        print(result.stderr)
    
    # Check if build was successful
    if os.path.exists(os.path.join('dist', 'CodePromptOptimizer.exe')):
        print("\nBuild successful! Executable created at: dist/CodePromptOptimizer.exe")
    else:
        print("\nBuild failed! Executable not created.")

if __name__ == '__main__':
    build_executable() 