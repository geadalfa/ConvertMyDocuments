$WshShell = New-Object -ComObject WScript.Shell
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = [Environment]::GetFolderPath("Desktop")

# Remove old shortcut if present
$oldLnk = Join-Path $DesktopDir "DocShield Converter.lnk"
if (Test-Path $oldLnk) {
    Remove-Item -Path $oldLnk -Force
}

# Create ConvertMyDocuments shortcut
$Shortcut = $WshShell.CreateShortcut((Join-Path $DesktopDir "ConvertMyDocuments.lnk"))
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"$(Join-Path $ProjectDir 'launch_convertmydocuments.vbs')`""
$Shortcut.WorkingDirectory = $ProjectDir
$Shortcut.Description = "ConvertMyDocuments v1.1.0 - Zero-Leakage Offline Document and OCR Suite"
$Shortcut.IconLocation = "$(Join-Path $ProjectDir 'app_icon.ico'),0"
$Shortcut.Save()
Write-Host "ConvertMyDocuments shortcut created successfully on Desktop!"
