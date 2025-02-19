import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_windows_installer():
    """Create Windows standalone installer with embedded Python."""
    print("Creating Windows standalone installer...")
    
    # Create PyInstaller spec file
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['token_script_v2.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),
        ('LICENSE', '.'),
        ('requirements.txt', '.'),
    ],
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

# Add NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
for root, dirs, files in os.walk(nltk_data_path):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, nltk_data_path)
        a.datas += [(f'nltk_data/{rel_path}', file_path, 'DATA')]

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
)
"""
    
    with open('CodePromptOptimizer.spec', 'w') as f:
        f.write(spec_content)
    
    # Build the executable
    subprocess.run(['pyinstaller', 'CodePromptOptimizer.spec', '--clean'])
    
    # Create installer using NSIS
    nsis_script = """
!include "MUI2.nsh"
!include "FileFunc.nsh"

Name "Code Prompt Optimizer"
OutFile "CodePromptOptimizer_Setup.exe"
InstallDir "$PROGRAMFILES\\Code Prompt Optimizer"
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
SectionEnd
"""
    
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    
    # Build the installer
    subprocess.run(['makensis', 'installer.nsi'])
    
    # Move the installer to the output directory
    os.makedirs('output', exist_ok=True)
    shutil.move('CodePromptOptimizer_Setup.exe', 'output/CodePromptOptimizer_Setup.exe')
    
    print("Windows installer created successfully!")

def create_macos_app():
    """Create macOS .app bundle with embedded Python."""
    print("Creating macOS application bundle...")
    
    # Create PyInstaller spec file for macOS
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['token_script_v2.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('requirements.txt', '.'),
    ],
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

# Add NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
for root, dirs, files in os.walk(nltk_data_path):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, nltk_data_path)
        a.datas += [(f'nltk_data/{rel_path}', file_path, 'DATA')]

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
    bundle_identifier='com.codepromptoptimizer'
)
"""
    
    with open('CodePromptOptimizer_macOS.spec', 'w') as f:
        f.write(spec_content)
    
    # Build the .app bundle
    subprocess.run(['pyinstaller', 'CodePromptOptimizer_macOS.spec', '--clean'])
    
    # Create DMG (optional)
    try:
        subprocess.run(['hdiutil', 'create', '-volname', 'Code Prompt Optimizer', 
                       '-srcfolder', 'dist/CodePromptOptimizer.app', 
                       '-ov', '-format', 'UDZO', 
                       'output/CodePromptOptimizer.dmg'])
        print("macOS DMG created successfully!")
    except Exception as e:
        print(f"Warning: Could not create DMG: {e}")
        print("The .app bundle is still available in the dist directory.")

def main():
    """Create standalone installers for different platforms."""
    os.makedirs('output', exist_ok=True)
    
    if sys.platform.startswith('win'):
        create_windows_installer()
    elif sys.platform.startswith('darwin'):
        create_macos_app()
    else:
        print("Linux standalone installer creation is not supported yet.")
        print("Please use the Python version installer for Linux systems.")

if __name__ == "__main__":
    main() 