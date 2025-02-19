import os
import sys
import subprocess
import shutil
from pathlib import Path

def copy_required_files(target_dir):
    """Copy required files to the target directory."""
    root_dir = Path(__file__).parent.parent.parent
    files_to_copy = {
        'src/token_script_v2.py': 'token_script_v2.py',
        'assets/icon.ico': 'icon.ico',
        'LICENSE': 'LICENSE',
        'requirements.txt': 'requirements.txt',
    }
    
    for src, dst in files_to_copy.items():
        src_path = root_dir / src
        if src_path.exists():
            shutil.copy2(src_path, target_dir / dst)
        else:
            print(f"Warning: {src} not found")

def create_windows_installer():
    """Create Windows standalone installer with embedded Python."""
    print("Creating Windows standalone installer...")
    
    # Create working directory
    work_dir = Path(__file__).parent / 'windows' / 'build'
    work_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy required files
    copy_required_files(work_dir)
    
    # Create PyInstaller spec file
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import os
import nltk

block_cipher = None

# Download NLTK data before creating the spec
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
nltk_data = []
for root, dirs, files in os.walk(nltk_data_path):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, nltk_data_path)
        nltk_data.append((f'nltk_data/{rel_path}', file_path, 'DATA'))

a = Analysis(
    ['token_script_v2.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),
        ('LICENSE', '.'),
        ('requirements.txt', '.'),
    ] + nltk_data,
    hiddenimports=['tiktoken', 'nltk', 'tkinter'],
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
    icon='icon.ico'
)"""
    
    spec_file = work_dir / 'CodePromptOptimizer.spec'
    spec_file.write_text(spec_content)
    
    # Build the executable
    subprocess.run(['pyinstaller', str(spec_file), '--clean'], cwd=str(work_dir))
    
    # Create NSIS installer script
    nsis_script = """!include "MUI2.nsh"
!include "FileFunc.nsh"

Name "Code Prompt Optimizer"
OutFile "CodePromptOptimizer_Setup.exe"
InstallDir "$PROGRAMFILES64\\Code Prompt Optimizer"
RequestExecutionLevel admin

!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    
    File "dist\\CodePromptOptimizer.exe"
    File "icon.ico"
    File "LICENSE"
    
    CreateDirectory "$SMPROGRAMS\\Code Prompt Optimizer"
    CreateShortCut "$SMPROGRAMS\\Code Prompt Optimizer\\Code Prompt Optimizer.lnk" "$INSTDIR\\CodePromptOptimizer.exe"
    CreateShortCut "$DESKTOP\\Code Prompt Optimizer.lnk" "$INSTDIR\\CodePromptOptimizer.exe"
    
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "DisplayName" "Code Prompt Optimizer"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "UninstallString" "$INSTDIR\\Uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "DisplayIcon" "$INSTDIR\\icon.ico"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\CodePromptOptimizer.exe"
    Delete "$INSTDIR\\icon.ico"
    Delete "$INSTDIR\\LICENSE"
    Delete "$INSTDIR\\Uninstall.exe"
    
    Delete "$SMPROGRAMS\\Code Prompt Optimizer\\Code Prompt Optimizer.lnk"
    Delete "$DESKTOP\\Code Prompt Optimizer.lnk"
    RMDir "$SMPROGRAMS\\Code Prompt Optimizer"
    RMDir "$INSTDIR"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer"
SectionEnd"""
    
    nsis_file = work_dir / 'installer.nsi'
    nsis_file.write_text(nsis_script)
    
    # Build the installer
    subprocess.run(['makensis', str(nsis_file)], cwd=str(work_dir))
    
    # Move installer to output directory
    output_dir = Path(__file__).parent / 'windows' / 'output'
    output_dir.mkdir(exist_ok=True)
    
    installer = work_dir / 'CodePromptOptimizer_Setup.exe'
    if installer.exists():
        shutil.move(installer, output_dir / 'CodePromptOptimizer_Setup.exe')
        print(f"Windows installer created successfully: {output_dir / 'CodePromptOptimizer_Setup.exe'}")
    else:
        print("Error: Installer creation failed")

def create_macos_installer():
    """Create macOS standalone installer."""
    print("Creating macOS installer...")
    
    # Create working directory
    work_dir = Path(__file__).parent / 'macos' / 'build'
    work_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy required files
    copy_required_files(work_dir)
    
    # Create PyInstaller spec file
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import os
import nltk

block_cipher = None

# Download NLTK data before creating the spec
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
nltk_data = []
for root, dirs, files in os.walk(nltk_data_path):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, nltk_data_path)
        nltk_data.append((f'nltk_data/{rel_path}', file_path, 'DATA'))

a = Analysis(
    ['token_script_v2.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('requirements.txt', '.'),
    ] + nltk_data,
    hiddenimports=['tiktoken', 'nltk', 'tkinter'],
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
)

app = BUNDLE(
    exe,
    name='CodePromptOptimizer.app',
    icon=None,
    bundle_identifier='com.codepromptoptimizer',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True'
    }
)"""
    
    spec_file = work_dir / 'CodePromptOptimizer.spec'
    spec_file.write_text(spec_content)
    
    # Build the .app bundle
    subprocess.run(['pyinstaller', str(spec_file), '--clean'], cwd=str(work_dir))
    
    # Create output directory
    output_dir = Path(__file__).parent / 'macos' / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Create DMG
    if sys.platform == 'darwin':
        try:
            app_path = work_dir / 'dist' / 'CodePromptOptimizer.app'
            dmg_path = output_dir / 'CodePromptOptimizer.dmg'
            
            subprocess.run([
                'hdiutil', 'create',
                '-volname', 'Code Prompt Optimizer',
                '-srcfolder', str(app_path),
                '-ov', '-format', 'UDZO',
                str(dmg_path)
            ])
            print(f"macOS DMG created successfully: {dmg_path}")
        except Exception as e:
            print(f"Warning: Could not create DMG: {e}")
            # Copy .app bundle as fallback
            if app_path.exists():
                shutil.copytree(app_path, output_dir / 'CodePromptOptimizer.app', dirs_exist_ok=True)
                print(f"macOS .app bundle copied to: {output_dir / 'CodePromptOptimizer.app'}")
    else:
        print("Note: DMG creation is only supported on macOS systems")
        print("The .app bundle is available in the dist directory")

def main():
    """Create standalone installers for different platforms."""
    if sys.platform.startswith('win'):
        create_windows_installer()
    elif sys.platform.startswith('darwin'):
        create_macos_installer()
    else:
        print("Error: This script must be run on Windows or macOS")
        print("Linux standalone installer creation is not supported")
        sys.exit(1)

if __name__ == "__main__":
    main() 