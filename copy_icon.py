#!/usr/bin/env python3
"""
Utility script to copy the icon file to the local directory for easier access.
This ensures the icon is available when packaging the application.
"""

import os
import shutil
from pathlib import Path
import sys

def main():
    # Source icon path provided by the user
    source_icon_path = Path(r"C:\Users\sethk\OneDrive\Documents\tokenizerv2-github\icon.ico")
    
    # Destination is the current directory
    dest_icon_path = Path("icon.ico")
    
    if not source_icon_path.exists():
        print(f"Error: Source icon not found at {source_icon_path}")
        return False
        
    # Check if already in the right place
    if source_icon_path.resolve() == dest_icon_path.resolve():
        print(f"Icon is already in the correct location: {dest_icon_path}")
        
        # Still copy to dist directory if it exists
        dist_dir = Path("dist")
        if dist_dir.exists():
            dist_icon_path = dist_dir / "icon.ico"
            if not dist_icon_path.exists():
                try:
                    shutil.copy2(source_icon_path, dist_icon_path)
                    print(f"Copied icon to dist directory: {dist_icon_path}")
                except Exception as e:
                    print(f"Error copying to dist directory: {e}")
        
        return True
        
    try:
        # Make a copy of the icon file in the current directory
        shutil.copy2(source_icon_path, dest_icon_path)
        print(f"Successfully copied icon from {source_icon_path} to {dest_icon_path}")
        
        # Also copy to dist directory if it exists (for standalone executable)
        dist_dir = Path("dist")
        if dist_dir.exists():
            dist_icon_path = dist_dir / "icon.ico"
            shutil.copy2(source_icon_path, dist_icon_path)
            print(f"Also copied icon to dist directory: {dist_icon_path}")
            
        return True
    except Exception as e:
        print(f"Error copying icon file: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 