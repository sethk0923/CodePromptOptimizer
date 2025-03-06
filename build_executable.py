#!/usr/bin/env python3
"""
Build script for compiling the Code Prompt Optimizer into a standalone executable.
This script uses PyInstaller to create a single executable that includes all dependencies.
"""

import os
import sys
import shutil
import platform
import subprocess
import site
from pathlib import Path

def main():
    print("===== Code Prompt Optimizer Build Script =====")
    print(f"Platform: {platform.system()} {platform.release()}")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("ERROR: PyInstaller not found. Install with 'pip install pyinstaller'")
        return False
    
    # Create build directory
    build_dir = Path("build")
    if not build_dir.exists():
        build_dir.mkdir()
        print("Created build directory.")
    
    # Create dist directory if it doesn't exist
    dist_dir = Path("dist")
    if not dist_dir.exists():
        dist_dir.mkdir()
        print("Created dist directory.")
    
    # Check for nltk_data
    nltk_data_dir = Path(site.getsitepackages()[0]) / "nltk_data"
    if not nltk_data_dir.exists():
        try:
            print("Downloading NLTK data...")
            import nltk
            nltk.download('words', quiet=True)
            print("NLTK data downloaded successfully.")
        except Exception as e:
            print(f"Warning: Could not download NLTK data: {e}")
            print("The built application may have limited autocomplete functionality.")
    
    # Check for Tree-sitter grammars
    ts_grammar_dir = Path("tree-sitter-grammars")
    has_ts_grammars = False
    if ts_grammar_dir.exists() and any(ts_grammar_dir.glob("*.so")):
        has_ts_grammars = True
        print(f"Found Tree-sitter grammars in {ts_grammar_dir}")
    else:
        print("No Tree-sitter grammars found. The application will fall back to regex parsing.")
        print("To use Tree-sitter, create a 'tree-sitter-grammars' directory with compiled language .so files.")
    
    # Check for Ghidra installation
    import importlib.util
    spec = importlib.util.find_spec("token_script_v3")
    if spec:
        try:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            import token_script_v3
            if hasattr(token_script_v3, 'GHIDRA_HEADLESS_PATH') and token_script_v3.GHIDRA_HEADLESS_PATH:
                print(f"Found Ghidra at: {token_script_v3.GHIDRA_HEADLESS_PATH}")
                print("Note: Ghidra will NOT be bundled with the executable.")
                print("Users will need to install Ghidra separately to use the decompilation features.")
            else:
                print("Ghidra not found. The application will fall back to basic binary analysis.")
                print("To use Ghidra, install it and ensure the analyzeHeadless script is in the PATH")
                print("or set the GHIDRA_HOME environment variable.")
        except ImportError:
            print("Could not import token_script_v3 module to check Ghidra.")
    
    # Create an icon file if it doesn't exist
    custom_icon_path = Path(r"C:\Users\sethk\OneDrive\Documents\tokenizerv2-github\icon.ico")
    icon_path = custom_icon_path if custom_icon_path.exists() else Path("icon.ico")
    
    if not icon_path.exists():
        try:
            # Try to create a simple icon using tkinter
            import tkinter as tk
            from PIL import Image, ImageDraw
            
            print("Creating default icon...")
            # Create a simple icon - a blue circle with 'CPO' text
            img = Image.new('RGBA', (256, 256), color=(0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.ellipse((20, 20, 236, 236), fill=(45, 45, 75))
            img.save('icon.png')
            
            # Convert PNG to ICO (Windows)
            if platform.system() == "Windows":
                img.save('icon.ico')
                print("Created icon.ico")
            else:
                print("Created icon.png")
        except Exception as e:
            print(f"Warning: Could not create default icon: {e}")
            print("The executable will use the default PyInstaller icon.")
    else:
        print(f"Using existing icon from: {icon_path}")
    
    # Build command
    cmd = ["pyinstaller", "--clean", "--onefile"]
    
    # Add icon if it exists
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    # Add Tree-sitter grammars if they exist
    if has_ts_grammars:
        ts_data_path = f"tree-sitter-grammars{os.pathsep}."
        cmd.extend(["--add-data", ts_data_path])
    
    # Add NLTK data location if it exists
    if nltk_data_dir.exists():
        nltk_path = f"{nltk_data_dir}{os.pathsep}nltk_data"
        cmd.extend(["--add-data", nltk_path])
    
    # Add main script
    cmd.append("token_script_v3.py")
    
    # Run PyInstaller
    print("\nRunning PyInstaller with command:")
    print(" ".join(cmd))
    print("\nThis may take several minutes...\n")
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild completed successfully!")
        print(f"Executable created in {dist_dir}")
        
        # Create a README about Ghidra integration
        ghidra_readme = Path(dist_dir) / "GHIDRA_INTEGRATION.txt"
        with open(ghidra_readme, 'w') as f:
            f.write("""
GHIDRA INTEGRATION
=================

The Code Prompt Optimizer supports advanced binary decompilation using Ghidra,
but Ghidra itself is NOT bundled with this executable due to its size.

To use the Ghidra integration:

1. Download and install Ghidra from https://ghidra-sre.org/
2. Ensure the Ghidra installation is in a standard location:
   - Windows: C:\\Program Files\\Ghidra or C:\\Ghidra
   - Linux/macOS: /opt/ghidra, /usr/local/ghidra, or ~/ghidra
   OR
3. Set the GHIDRA_HOME environment variable to your Ghidra installation directory

The application will automatically detect Ghidra and use it for binary analysis
if available. If Ghidra is not found, the application will fall back to basic
binary analysis using pefile and other libraries.
""")
        
        # Rename the executable to a nicer name
        executable_ext = ".exe" if platform.system() == "Windows" else ""
        orig_name = dist_dir / f"token_script_v3{executable_ext}"
        new_name = dist_dir / f"CodePromptOptimizer_v3{executable_ext}"
        
        if orig_name.exists():
            try:
                shutil.move(orig_name, new_name)
                print(f"Renamed executable to {new_name.name}")
            except Exception as e:
                print(f"Warning: Could not rename executable: {e}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Build failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"Error: Build failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 