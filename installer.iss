[Setup]
AppName=Flash Convert
AppVersion=1.0.0
AppPublisher=Flash Convert
DefaultDirName={autopf}\FlashConvert
DefaultGroupName=Flash Convert
UninstallDisplayIcon={app}\flash_convert.exe
OutputDir=installer_output
OutputBaseFilename=FlashConvert_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "dist\flash_convert.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; Parent cascading menu entry
Root: HKCR; Subkey: "SystemFileAssociations\.heic\shell\FlashConvert"; ValueType: string; ValueName: "MUIVerb"; ValueData: "Flash HEIC Convert"; Flags: uninsdeletekey
Root: HKCR; Subkey: "SystemFileAssociations\.heic\shell\FlashConvert"; ValueType: string; ValueName: "SubCommands"; ValueData: "FlashConvert.ToPNG;FlashConvert.ToJPG"
Root: HKCR; Subkey: "SystemFileAssociations\.heic\shell\FlashConvert"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\flash_convert.exe,0"

; CommandStore: "to PNG"
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\FlashConvert.ToPNG"; ValueType: string; ValueName: ""; ValueData: "to PNG"; Flags: uninsdeletekey
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\FlashConvert.ToPNG\command"; ValueType: string; ValueName: ""; ValueData: """{app}\flash_convert.exe"" ""%1"" png"

; CommandStore: "to JPG"
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\FlashConvert.ToJPG"; ValueType: string; ValueName: ""; ValueData: "to JPG"; Flags: uninsdeletekey
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\FlashConvert.ToJPG\command"; ValueType: string; ValueName: ""; ValueData: """{app}\flash_convert.exe"" ""%1"" jpg"
