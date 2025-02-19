import os
import sys
import shutil
import subprocess
from pathlib import Path
import zipfile
import datetime

def create_standalone_installer():
    """Creates a standalone EXE installer that doesn't require Python."""
    print("Creating standalone installer...")
    
    # Create the NSIS installer script
    with open("installer.nsi", "w") as f:
        f.write("""
; Code Prompt Optimizer Installer Script
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Define installer name and metadata
Name "Code Prompt Optimizer"
OutFile "CodePromptOptimizer_Setup.exe"
InstallDir "$PROGRAMFILES\\Code Prompt Optimizer"
BrandingText "Code Prompt Optimizer Installer"

; Add version info
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "Code Prompt Optimizer"
VIAddVersionKey "FileDescription" "AI Prompt Optimization Tool"
VIAddVersionKey "LegalCopyright" "© 2024"
VIAddVersionKey "FileVersion" "1.0.0.0"

; Modern interface settings
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "installer_splash.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "installer_header.bmp"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Set the language
!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    
    ; Add files
    File "dist\\CodePromptOptimizer.exe"
    File "icon.ico"
    File "LICENSE"
    File "standalone_install_readme.txt"
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\\Code Prompt Optimizer.lnk" "$INSTDIR\\CodePromptOptimizer.exe" "" "$INSTDIR\\icon.ico"
    
    ; Create start menu shortcuts
    CreateDirectory "$SMPROGRAMS\\Code Prompt Optimizer"
    CreateShortCut "$SMPROGRAMS\\Code Prompt Optimizer\\Code Prompt Optimizer.lnk" "$INSTDIR\\CodePromptOptimizer.exe" "" "$INSTDIR\\icon.ico"
    CreateShortCut "$SMPROGRAMS\\Code Prompt Optimizer\\Readme.lnk" "$INSTDIR\\standalone_install_readme.txt"
    CreateShortCut "$SMPROGRAMS\\Code Prompt Optimizer\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
    
    ; Write uninstaller
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
    
    ; Add uninstall information to Add/Remove Programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "DisplayName" "Code Prompt Optimizer"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "UninstallString" "$INSTDIR\\Uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "DisplayIcon" "$INSTDIR\\icon.ico"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "Publisher" "Your Company"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "DisplayVersion" "1.0.0"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer" "NoRepair" 1
SectionEnd

Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\\CodePromptOptimizer.exe"
    Delete "$INSTDIR\\icon.ico"
    Delete "$INSTDIR\\LICENSE"
    Delete "$INSTDIR\\standalone_install_readme.txt"
    Delete "$INSTDIR\\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$DESKTOP\\Code Prompt Optimizer.lnk"
    Delete "$SMPROGRAMS\\Code Prompt Optimizer\\Code Prompt Optimizer.lnk"
    Delete "$SMPROGRAMS\\Code Prompt Optimizer\\Readme.lnk"
    Delete "$SMPROGRAMS\\Code Prompt Optimizer\\Uninstall.lnk"
    RMDir "$SMPROGRAMS\\Code Prompt Optimizer"
    
    ; Remove installation directory
    RMDir "$INSTDIR"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\CodePromptOptimizer"
SectionEnd
""")

def create_distribution_package():
    """Creates both Python-dependent and standalone installation packages."""
    print("Creating distribution packages...")
    
    # Create version info file
    version_info = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
         StringStruct(u'FileDescription', u'Code Prompt Optimizer'),
         StringStruct(u'FileVersion', u'1.0.0'),
         StringStruct(u'InternalName', u'code_prompt_optimizer'),
         StringStruct(u'LegalCopyright', u'© 2024 Your Company'),
         StringStruct(u'OriginalFilename', u'CodePromptOptimizer.exe'),
         StringStruct(u'ProductName', u'Code Prompt Optimizer'),
         StringStruct(u'ProductVersion', u'1.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    with open("version_info.txt", "w") as f:
        f.write(version_info)
    
    # First, create the executable using PyInstaller with version info
    subprocess.run([
        "pyinstaller",
        "--name=CodePromptOptimizer",
        "--onefile",
        "--windowed",
        "--icon=icon.ico",
        "--version-file=version_info.txt",
        "--add-data=icon.ico;.",
        "--add-data=LICENSE;.",
        "token_script_v2.py"
    ])
    
    # Create standalone installer
    create_standalone_installer()
    
    # Create directory for distribution files
    os.makedirs("dist/python_install", exist_ok=True)
    os.makedirs("dist/standalone_install", exist_ok=True)
    
    # Copy files for Python-dependent installation
    python_files = [
        ("install.bat", "dist/python_install/"),
        ("uninstall.bat", "dist/python_install/"),
        ("requirements.txt", "dist/python_install/"),
        ("token_script_v2.py", "dist/python_install/"),
        ("icon.ico", "dist/python_install/"),
        ("python_install_readme.txt", "dist/python_install/README.txt"),
        ("LICENSE", "dist/python_install/")
    ]
    
    for src, dst in python_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    # Copy files for standalone installation
    standalone_files = [
        ("dist/CodePromptOptimizer.exe", "dist/standalone_install/"),
        ("icon.ico", "dist/standalone_install/"),
        ("standalone_install_readme.txt", "dist/standalone_install/README.txt"),
        ("LICENSE", "dist/standalone_install/")
    ]
    
    for src, dst in standalone_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    # Create ZIP files with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    
    def create_zip(source_dir, zip_name):
        with zipfile.ZipFile(f"dist/{zip_name}", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    create_zip("dist/python_install", f"CodePromptOptimizer_Python_{timestamp}.zip")
    create_zip("dist/standalone_install", f"CodePromptOptimizer_Standalone_{timestamp}.zip")
    
    # Create NSIS installer if NSIS is installed
    try:
        subprocess.run(["makensis", "installer.nsi"])
        shutil.move("CodePromptOptimizer_Setup.exe", f"dist/CodePromptOptimizer_Setup_{timestamp}.exe")
        print(f"\nStandalone installer created successfully: dist/CodePromptOptimizer_Setup_{timestamp}.exe")
    except FileNotFoundError:
        print("\nNSIS not found. Standalone installer could not be created.")
        print("To create the standalone installer, please install NSIS from https://nsis.sourceforge.io/Download")
    
    # Clean up temporary files
    for file in ["version_info.txt", "installer.nsi"]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\nDistribution packages created:")
    print(f"1. dist/CodePromptOptimizer_Python_{timestamp}.zip - For users with Python installed")
    print(f"2. dist/CodePromptOptimizer_Standalone_{timestamp}.zip - For users without Python")
    print("\nAll distribution files are in the 'dist' directory.")

if __name__ == "__main__":
    create_distribution_package() 