; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "TS2"
!define PRODUCT_VERSION "0.4"
!define PRODUCT_PUBLISHER "NPi"
!define PRODUCT_WEB_SITE "http://ts2.sf.net"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\ts2.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!define MUI_LICENSEPAGE_RADIOBUTTONS
!insertmacro MUI_PAGE_LICENSE "build\exe.win-amd64-3.3\doc\COPYING.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\ts2.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\doc\README.txt"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "French"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "dist\${PRODUCT_NAME}-${PRODUCT_VERSION}-x64-setup.exe"
InstallDir "$PROGRAMFILES64\TS2"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

Section "SectionPrincipale" SEC01
  SetOutPath "$INSTDIR\doc"
  SetOverwrite try
  File "build\exe.win-amd64-3.3\doc\COPYING.txt"
  File "build\exe.win-amd64-3.3\doc\README.txt"
  File "build\exe.win-amd64-3.3\doc\README_fr.txt"
  SetOutPath "$INSTDIR"
  File "build\exe.win-amd64-3.3\LIBEAY32.dll"
  File "build\exe.win-amd64-3.3\library.zip"
  File "build\exe.win-amd64-3.3\msvcp100.dll"
  File "build\exe.win-amd64-3.3\MSVCR100.dll"
  File "build\exe.win-amd64-3.3\PyQt4.Qt.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtCore.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtGui.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtNetwork.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtOpenGL.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtScript.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtSql.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtSvg.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtTest.pyd"
  File "build\exe.win-amd64-3.3\PyQt4.QtXml.pyd"
  File "build\exe.win-amd64-3.3\python33.dll"
  File "build\exe.win-amd64-3.3\QtCore4.dll"
  File "build\exe.win-amd64-3.3\QtGui4.dll"
  File "build\exe.win-amd64-3.3\QtNetwork4.dll"
  File "build\exe.win-amd64-3.3\QtOpenGL4.dll"
  File "build\exe.win-amd64-3.3\QtScript4.dll"
  File "build\exe.win-amd64-3.3\QtSql4.dll"
  File "build\exe.win-amd64-3.3\QtSvg4.dll"
  File "build\exe.win-amd64-3.3\QtTest4.dll"
  File "build\exe.win-amd64-3.3\QtXml4.dll"
  SetOutPath "$INSTDIR\simulations"
  File "build\exe.win-amd64-3.3\simulations\drain.ts2"
  File "build\exe.win-amd64-3.3\simulations\liverpool-st.ts2"
  SetOutPath "$INSTDIR\i18n"
  File "build\exe.win-amd64-3.3\i18n\ts2_fr.qm"
  SetOutPath "$INSTDIR"
  File "build\exe.win-amd64-3.3\sip.pyd"
  File "build\exe.win-amd64-3.3\sqlite3.dll"
  File "build\exe.win-amd64-3.3\SSLEAY32.dll"
  File "build\exe.win-amd64-3.3\ts2.exe"
  CreateDirectory "$SMPROGRAMS\Train Signalling Simulation"
  CreateShortCut "$SMPROGRAMS\Train Signalling Simulation\TS2.lnk" "$INSTDIR\ts2.exe"
  CreateShortCut "$DESKTOP\TS2.lnk" "$INSTDIR\ts2.exe"
  File "build\exe.win-amd64-3.3\unicodedata.pyd"
  File "build\exe.win-amd64-3.3\_bz2.pyd"
  File "build\exe.win-amd64-3.3\_sqlite3.pyd"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\Train Signalling Simulation\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\Train Signalling Simulation\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\ts2.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\ts2.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) has been removed from your computer"
FunctionEnd

Function un.onInit
!insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to uninstall $(^Name) completely ?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\_sqlite3.pyd"
  Delete "$INSTDIR\_bz2.pyd"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\ts2.exe"
  Delete "$INSTDIR\SSLEAY32.dll"
  Delete "$INSTDIR\sqlite3.dll"
  Delete "$INSTDIR\sip.pyd"
  Delete "$INSTDIR\simulations\liverpool-st.ts2"
  Delete "$INSTDIR\simulations\drain.ts2"
  Delete "$INSTDIR\QtXml4.dll"
  Delete "$INSTDIR\QtTest4.dll"
  Delete "$INSTDIR\QtSvg4.dll"
  Delete "$INSTDIR\QtSql4.dll"
  Delete "$INSTDIR\QtScript4.dll"
  Delete "$INSTDIR\QtOpenGL4.dll"
  Delete "$INSTDIR\QtNetwork4.dll"
  Delete "$INSTDIR\QtGui4.dll"
  Delete "$INSTDIR\QtCore4.dll"
  Delete "$INSTDIR\python33.dll"
  Delete "$INSTDIR\PyQt4.QtXml.pyd"
  Delete "$INSTDIR\PyQt4.QtTest.pyd"
  Delete "$INSTDIR\PyQt4.QtSvg.pyd"
  Delete "$INSTDIR\PyQt4.QtSql.pyd"
  Delete "$INSTDIR\PyQt4.QtScript.pyd"
  Delete "$INSTDIR\PyQt4.QtOpenGL.pyd"
  Delete "$INSTDIR\PyQt4.QtNetwork.pyd"
  Delete "$INSTDIR\PyQt4.QtGui.pyd"
  Delete "$INSTDIR\PyQt4.QtCore.pyd"
  Delete "$INSTDIR\PyQt4.Qt.pyd"
  Delete "$INSTDIR\MSVCR100.dll"
  Delete "$INSTDIR\msvcp100.dll"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\LIBEAY32.dll"
  Delete "$INSTDIR\doc\README.txt"
  Delete "$INSTDIR\doc\README_fr.txt"
  Delete "$INSTDIR\doc\COPYING.txt"

  Delete "$SMPROGRAMS\Train Signalling Simulation\Uninstall.lnk"
  Delete "$SMPROGRAMS\Train Signalling Simulation\Website.lnk"
  Delete "$DESKTOP\TS2.lnk"
  Delete "$SMPROGRAMS\Train Signalling Simulation\TS2.lnk"

  RMDir "$SMPROGRAMS\Train Signalling Simulation"
  RMDir "$INSTDIR\simulations"
  RMDir "$INSTDIR\doc"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd
