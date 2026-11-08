; Inno Setup Script untuk ConvertMyDocuments v1.1.0
; Menghasilkan installer mandiri profesional: ConvertMyDocuments_Setup_v1.1.0.exe

#define MyAppName "ConvertMyDocuments"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "geadalfa"
#define MyAppURL "https://github.com/geadalfa/ConvertMyDocuments"
#define MyAppExeName "ConvertMyDocuments.exe"

[Setup]
AppId={{D37F82C1-5B39-4E62-8E31-68F42A19E502}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=C:\Users\Alfa\.gemini\antigravity\scratch\docshield-converter\installer_output
OutputBaseFilename=ConvertMyDocuments_Setup_v1.1.0
SetupIconFile=C:\Users\Alfa\.gemini\antigravity\scratch\docshield-converter\app_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Alfa\.gemini\antigravity\scratch\docshield-converter\dist\ConvertMyDocuments\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Jalankan {#MyAppName} sekarang"; Flags: nowait postinstall skipifsilent
