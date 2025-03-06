"""
Create a ZIP file of the v2 distribution folder for easy sharing.
"""

import os
import zipfile
from pathlib import Path
import datetime

# Configure paths
current_dir = Path(os.getcwd())
dist_v2_dir = current_dir / 'dist_v2'
date_str = datetime.datetime.now().strftime("%Y%m%d")
zip_filename = f"CodePromptOptimizerv2_{date_str}.zip"
zip_path = current_dir / zip_filename

def create_zip():
    """Create a ZIP file of the dist_v2 folder"""
    if not dist_v2_dir.exists():
        print(f"ERROR: Distribution folder not found: {dist_v2_dir}")
        return
    
    print(f"Creating ZIP file: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dist_v2_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(dist_v2_dir.parent)
                print(f"Adding: {arcname}")
                zipf.write(file_path, arcname)
    
    print(f"\nZIP file created successfully: {zip_path}")
    print(f"Size: {os.path.getsize(zip_path) / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    create_zip() 