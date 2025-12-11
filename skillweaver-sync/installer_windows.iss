; Inno Setup Script for WoW Suite Sync

[Setup]
AppName=WoW Suite Sync
AppVersion=1.0.0
DefaultDirName={autopf}\WoWSuiteSync
DefaultGroupName=WoW Suite Sync
OutputDir=Output
OutputBaseFilename=WoWSuiteSync-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Files]
Source: "dist\WoWSuiteSync.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.ini.example"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\WoW Suite Sync"; Filename: "{app}\WoWSuiteSync.exe"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"
Name: "{userstartup}\WoW Suite Sync"; Filename: "{app}\WoWSuiteSync.exe"; Tasks: startupicon

[Tasks]
Name: "startupicon"; Description: "Start automatically when Windows starts"; GroupDescription: "Additional options:"

[Run]
Filename: "{app}\WoWSuiteSync.exe"; Description: "Launch WoW Suite Sync"; Flags: nowait postinstall skipifsilent
