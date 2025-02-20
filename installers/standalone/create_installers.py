import os
import sys
import subprocess
import shutil
import importlib.util
import importlib
import platform
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

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
    """Create Windows standalone installer with embedded Python."""
    print("Creating Windows standalone installer...")
    
    if not install_dependencies():
        print("Dependency installation failed.")
        return False

    try:
        # Create working directory
        work_dir = Path(__file__).parent / 'windows' / 'build'
        work_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if executable already exists
        exe_path = work_dir / 'dist' / 'CodePromptOptimizer.exe'
        if not exe_path.exists():
            # Copy required files
            print("Copying required files...")
            copy_required_files(work_dir)
            
            # Create PyInstaller spec file
            print("Creating PyInstaller spec file...")
            spec_content = """# -*- mode: python ; coding: utf-8 -*-

import os
import nltk
import site
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Download NLTK data before creating the spec
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Get site-packages directory
site_packages = site.getsitepackages()[0]

# Get transformers cache directory for GPT-2 tokenizer
transformers_cache = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'transformers')
transformers_data = []
if os.path.exists(transformers_cache):
    for root, dirs, files in os.walk(transformers_cache):
        if 'gpt2' in root.lower():
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, transformers_cache)
                transformers_data.append((f'transformers_cache/{rel_path}', file_path, 'DATA'))

# Get NLTK data
nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
nltk_data = []
for root, dirs, files in os.walk(nltk_data_path):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, nltk_data_path)
        nltk_data.append((f'nltk_data/{rel_path}', file_path, 'DATA'))

# Get tiktoken data files
tiktoken_data = collect_data_files('tiktoken')

# Get tiktoken cache directory
tiktoken_cache = os.path.join(os.path.expanduser('~'), '.cache', 'tiktoken')
if os.path.exists(tiktoken_cache):
    for root, dirs, files in os.walk(tiktoken_cache):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, tiktoken_cache)
            tiktoken_data.append((f'tiktoken_cache/{rel_path}', file_path, 'DATA'))

a = Analysis(
    ['token_script_v2.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('LICENSE', '.'),
        ('requirements.txt', '.'),
    ] + nltk_data + transformers_data + tiktoken_data,
    hiddenimports=[
        'tiktoken',
        'tiktoken.core',
        'tiktoken_ext',
        'tiktoken_ext.openai_public',
        'tiktoken.registry',
        'transformers',
        'transformers.models.gpt2',
        'transformers.models.gpt2.tokenization_gpt2',
        'transformers.utils',
        'transformers.tokenization_utils',
        'transformers.tokenization_utils_base',
        'nltk',
        'nltk.tokenize',
        'nltk.corpus',
        'tkinter',
        'requests'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)"""
            
            spec_file = work_dir / 'CodePromptOptimizer.spec'
            spec_file.write_text(spec_content)
            
            # Build the executable with debug output
            print("Building executable with PyInstaller...")
            result = subprocess.run(['pyinstaller', str(spec_file), '--clean'], cwd=str(work_dir), capture_output=True, text=True)
            if result.returncode != 0:
                print("PyInstaller build error:")
                print("stdout:", result.stdout)
                print("stderr:", result.stderr)
                return False
            print("✅ PyInstaller build successful.")
        else:
            print("Using existing executable...")
            
            # Copy required files if they don't exist
            root_dir = Path(__file__).parent.parent.parent
            files_to_copy = {
                'LICENSE': 'LICENSE',
            }
            
            for src, dst in files_to_copy.items():
                src_path = root_dir / src
                dst_path = work_dir / dst
                if src_path.exists() and not dst_path.exists():
                    print(f"Copying {src} to {dst}")
                    shutil.copy2(src_path, dst_path)
        
        # Create NSIS installer script
        print("Creating NSIS installer script...")
        nsis_script = r"""
; Include Modern UI
!include "MUI2.nsh"

; General
Name "Code Prompt Optimizer"
OutFile "CodePromptOptimizer_Setup.exe"
InstallDir "$PROGRAMFILES64\Code Prompt Optimizer"
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language
!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    
    ; Add files
    File "dist\CodePromptOptimizer.exe"
    File "LICENSE"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\Code Prompt Optimizer"
    CreateShortCut "$SMPROGRAMS\Code Prompt Optimizer\Code Prompt Optimizer.lnk" "$INSTDIR\CodePromptOptimizer.exe"
    
    ; Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Write registry keys
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "DisplayName" "Code Prompt Optimizer"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "UninstallString" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\CodePromptOptimizer.exe"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\Code Prompt Optimizer\Code Prompt Optimizer.lnk"
    RMDir "$SMPROGRAMS\Code Prompt Optimizer"
    RMDir "$INSTDIR"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer"
SectionEnd"""
        
        nsis_file = work_dir / 'installer.nsi'
        nsis_file.write_text(nsis_script)
        
        # Build the installer
        print("Building NSIS installer...")
        nsis_path = r'C:\Program Files (x86)\NSIS'
        result = subprocess.run([os.path.join(nsis_path, 'makensis.exe'), str(nsis_file)], cwd=str(work_dir), capture_output=True, text=True)
        if result.returncode != 0:
            print("Error building installer:")
            print(result.stderr)
            return False
        
        # Move installer to output directory
        output_dir = Path(__file__).parent / 'windows' / 'output'
        output_dir.mkdir(exist_ok=True)
        
        installer = work_dir / 'CodePromptOptimizer_Setup.exe'
        if installer.exists():
            shutil.move(installer, output_dir / 'CodePromptOptimizer_Setup.exe')
            print(f"✅ Windows installer created successfully: {output_dir / 'CodePromptOptimizer_Setup.exe'}")
            return True
        else:
            print("❌ Error: Installer creation failed - Setup file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error creating installer: {str(e)}")
        return False

def copy_required_files(work_dir):
    """Copy necessary files for the installer."""
    root_dir = Path(__file__).parent.parent.parent
    files_to_copy = {
        'token_script_v2.py': 'token_script_v2.py',
        'LICENSE': 'LICENSE',
        'requirements.txt': 'requirements.txt',
    }
    
    for src, dst in files_to_copy.items():
        src_path = root_dir / src
        if src_path.exists():
            shutil.copy2(src_path, work_dir / dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Warning: {src} not found at {src_path}")

def main():
    """Create standalone installers for different platforms."""
    if sys.platform.startswith('win'):
        create_windows_installer()
    else:
        print("Error: This script must be run on Windows")
        print("Other platforms are not supported")
        sys.exit(1)

if __name__ == "__main__":
    main()
