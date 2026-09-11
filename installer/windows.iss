#define MyAppName "Hashcat GUI"
#define MyAppVersion "1.4.0"
#define MyAppPublisher "Felix3214g"
#define MyAppExeName "HashcatGUI.exe"

[Setup]
AppId={{8C3A4D31-5F3B-47D4-B302-8A2A9EC69410}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Hashcat GUI
DefaultGroupName={#MyAppName}
UninstallDisplayName={#MyAppName}
OutputDir=..\installer-output
OutputBaseFilename=HashcatGUI-v1.4.0-windows-x64-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
