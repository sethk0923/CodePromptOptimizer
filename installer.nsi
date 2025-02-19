; Code Prompt Optimizer Installer Script
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Define installer name and metadata
Name "Code Prompt Optimizer"
OutFile "dist\CodePromptOptimizer_Setup.exe"
InstallDir "$PROGRAMFILES\Code Prompt Optimizer"
InstallDirRegKey HKLM "Software\Code Prompt Optimizer" "Install_Dir"
RequestExecutionLevel admin

; Version information
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "Code Prompt Optimizer"
VIAddVersionKey "CompanyName" "Your Company"
VIAddVersionKey "FileDescription" "AI Prompt Optimization Tool"
VIAddVersionKey "LegalCopyright" "© 2024"
VIAddVersionKey "FileVersion" "1.0.0"

; Modern UI settings
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

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
    File "dist\CodePromptOptimizer.exe"
    File "icon.ico"
    File "LICENSE"
    File "standalone_install_readme.txt"
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\Code Prompt Optimizer.lnk" "$INSTDIR\CodePromptOptimizer.exe" "" "$INSTDIR\icon.ico"
    
    ; Create start menu shortcuts
    CreateDirectory "$SMPROGRAMS\Code Prompt Optimizer"
    CreateShortCut "$SMPROGRAMS\Code Prompt Optimizer\Code Prompt Optimizer.lnk" "$INSTDIR\CodePromptOptimizer.exe" "" "$INSTDIR\icon.ico"
    CreateShortCut "$SMPROGRAMS\Code Prompt Optimizer\Readme.lnk" "$INSTDIR\standalone_install_readme.txt"
    CreateShortCut "$SMPROGRAMS\Code Prompt Optimizer\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    
    ; Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Write registry keys for Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "DisplayName" "Code Prompt Optimizer"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "DisplayIcon" "$INSTDIR\icon.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "Publisher" "Your Company"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "DisplayVersion" "1.0.0"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "NoRepair" 1
    
    ; Store installation folder
    WriteRegStr HKLM "Software\Code Prompt Optimizer" "Install_Dir" "$INSTDIR"
SectionEnd

Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\CodePromptOptimizer.exe"
    Delete "$INSTDIR\icon.ico"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\standalone_install_readme.txt"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$DESKTOP\Code Prompt Optimizer.lnk"
    Delete "$SMPROGRAMS\Code Prompt Optimizer\Code Prompt Optimizer.lnk"
    Delete "$SMPROGRAMS\Code Prompt Optimizer\Readme.lnk"
    Delete "$SMPROGRAMS\Code Prompt Optimizer\Uninstall.lnk"
    RMDir "$SMPROGRAMS\Code Prompt Optimizer"
    
    ; Remove installation directory
    RMDir "$INSTDIR"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer"
    DeleteRegKey HKLM "Software\Code Prompt Optimizer"
SectionEnd 