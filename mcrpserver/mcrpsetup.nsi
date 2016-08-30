;--------------------------------

; The name of the installer
Name "Microsemi CRP server"

; The file to write
OutFile "mcrpsetup.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\Microsemi CRP server"

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\Microsemi CRP server" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; Declaration of user variables (Var command), allowed charaters for variables names : [a-z][A-Z][0-9] and '_'

  Var "Name"

;--------------------------------

; The stuff to install
Section "Microsemi CRP server (required)"

  StrCpy "$Name" "Microsemi CRP server"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /nonfatal /r "dist\mcrpserver\"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM "SOFTWARE\$Name" "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$Name" "DisplayName" "$Name"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$Name" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$Name" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$Name" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)

Section "Desktop Shortcuts"

  CreateShortCut "$DESKTOP\$Name.lnk" "$INSTDIR\mcrpserver.exe" "" "$INSTDIR\mcrpserver.exe" 0
  
SectionEnd

Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\$Name"
  CreateShortCut "$SMPROGRAMS\$Name\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\$Name\$Name.lnk" "$INSTDIR\mcrpserver.exe" "" "$INSTDIR\mcrpserver.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"

  StrCpy "$Name" "Microsemi CRP server"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$Name"
  DeleteRegKey HKLM SOFTWARE\$Name

  ; Remove files and uninstaller
  Delete $INSTDIR\*.*

  ; Remove shortcuts, if any
  Delete "$DESKTOP\$Name.lnk"
  Delete "$SMPROGRAMS\$Name\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\$Name"
  RMDir /r "$INSTDIR"

SectionEnd
