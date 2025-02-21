import os
import sys
import subprocess
import shutil
import importlib.util
import importlib
import platform
from pathlib import Path

def check_tiktoken_version():
    """Check if tiktoken is installed and return its version."""
    try:
        spec = importlib.util.find_spec("tiktoken")
        if spec is None:
            return None
        version_output = subprocess.run(
            [sys.executable, "-m", "pip", "show", "tiktoken"],
            capture_output=True, text=True
        ).stdout
        for line in version_output.splitlines():
            if line.startswith("Version:"):
                return line.split("Version:")[-1].strip()
    except Exception:
        return None

def install_tiktoken():
    """Ensure tiktoken is installed at version 0.9.0."""
    required_version = "0.9.0"
    current_version = check_tiktoken_version()

    if current_version == required_version:
        print(f"✅ tiktoken {required_version} is already installed.")
        return True

    print(f"🔄 Installing tiktoken {required_version} (current: {current_version})...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-cache-dir", f"tiktoken=={required_version}"], check=True)
        return check_tiktoken_version() == required_version
    except subprocess.CalledProcessError:
        return False

def verify_cl100k_base():
    """Verify if cl100k_base encoding is available."""
    try:
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        test_result = encoding.encode("test")
        print(f"✅ cl100k_base encoding loaded. Test result: {test_result}")
        return True
    except Exception as e:
        print(f"❌ Error loading cl100k_base encoding: {e}")
        return False

def install_dependencies():
    """Install required dependencies."""
    dependencies = ["pyinstaller", "transformers"]
    
    if not install_tiktoken() or not verify_cl100k_base():
        print("❌ tiktoken setup failed.")
        return False
    
    for package in dependencies:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package], check=True)
        except subprocess.CalledProcessError:
            print(f"Error installing {package}")
            return False
    
    return True

def create_windows_installer():
    """Create a Windows standalone installer."""
    if not install_dependencies():
        print("Dependency installation failed.")
        return False
    
    work_dir = Path(__file__).parent / 'windows' / 'build'
    work_dir.mkdir(parents=True, exist_ok=True)
    
    script_path = Path(__file__).parent / ".." / ".." / "token_script_v2.py"
    print(f"Script path: {script_path}")
    print(f"Script exists: {script_path.exists()}")
    
    if not script_path.exists():
        print("Error: Could not find token_script_v2.py")
        return False
    
    spec_file = work_dir / 'CodePromptOptimizer.spec'
    print(f"Spec file path: {spec_file}")
    
    # Get NLTK data directory
    import nltk
    nltk_data_dir = Path(nltk.data.path[0])
    print(f"NLTK data dir: {nltk_data_dir}")
    
    # Generate the .spec file dynamically
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

# Get NLTK data paths
nltk_data = [
    ('punkt', 'tokenizers/punkt'),
    ('stopwords', 'corpora/stopwords'),
    ('averaged_perceptron_tagger', 'taggers/averaged_perceptron_tagger')
]

nltk_data_path = r'{nltk_data_dir}'
datas = []
for package, subdir in nltk_data:
    data_dir = os.path.join(nltk_data_path, subdir)
    if os.path.exists(data_dir):
        datas.append((data_dir, subdir))

print("NLTK data paths:", datas)

a = Analysis(
    [r'{script_path}'],
    pathex=[r'{work_dir}'],
    binaries=[],
    datas=datas,
    hiddenimports=['tiktoken', 'tiktoken_ext.openai_public', 'nltk', 'transformers',
                   'nltk.tokenize', 'nltk.corpus', 'nltk.tag',
                   'nltk.tokenize.punkt', 'nltk.corpus.stopwords'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None
)

print("Analysis complete")

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

print("PYZ complete")

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CodePromptOptimizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True temporarily for debugging
    icon=None
)

print("EXE complete")
    """
    
    print("Writing spec file...")
    spec_file.write_text(spec_content)
    print("Spec file written")
    
    print("Running PyInstaller...")
    pyinstaller_cmd = ["pyinstaller", str(spec_file), "--clean", "--log-level", "DEBUG"]
    result = subprocess.run(pyinstaller_cmd, cwd=str(work_dir), capture_output=True, text=True)
    
    print("PyInstaller stdout:")
    print(result.stdout)
    print("\nPyInstaller stderr:")
    print(result.stderr)
    
    if result.returncode != 0:
        print("PyInstaller build error:", result.stderr)
        return False
    
    print("✅ PyInstaller build successful.")
    return True

def main():
    if sys.platform.startswith('win'):
        create_windows_installer()
    else:
        print("Error: This script must be run on Windows")
        sys.exit(1)

if __name__ == "__main__":
    main()
