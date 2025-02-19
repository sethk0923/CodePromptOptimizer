
; Code Prompt Optimizer Installer Script
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Define installer name
Name "Code Prompt Optimizer"
OutFile "CodePromptOptimizer_Setup.exe"
InstallDir "$PROGRAMFILES\Code Prompt Optimizer"

; Modern interface settings
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
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
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\Code Prompt Optimizer.lnk" "$INSTDIR\CodePromptOptimizer.exe"
    
    ; Create start menu shortcut
    CreateDirectory "$SMPROGRAMS\Code Prompt Optimizer"
    CreateShortCut "$SMPROGRAMS\Code Prompt Optimizer\Code Prompt Optimizer.lnk" "$INSTDIR\CodePromptOptimizer.exe"
    
    ; Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Add uninstall information to Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "DisplayName" "Code Prompt Optimizer"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer" "DisplayIcon" "$INSTDIR\icon.ico"
SectionEnd

Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\CodePromptOptimizer.exe"
    Delete "$INSTDIR\icon.ico"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$DESKTOP\Code Prompt Optimizer.lnk"
    Delete "$SMPROGRAMS\Code Prompt Optimizer\Code Prompt Optimizer.lnk"
    RMDir "$SMPROGRAMS\Code Prompt Optimizer"
    
    ; Remove installation directory
    RMDir "$INSTDIR"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CodePromptOptimizer"
SectionEnd
