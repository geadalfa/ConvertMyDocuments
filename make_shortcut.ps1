$WshShell = New-Object -ComObject WScript.Shell

# Remove old shortcut if present
$oldLnk = "C:\Users\Alfa\Desktop\DocShield Converter.lnk"
if (Test-Path $oldLnk) {
    Remove-Item -Path $oldLnk -Force
}

# Create ConvertMyDocuments shortcut
$Shortcut = $WshShell.CreateShortcut("C:\Users\Alfa\Desktop\ConvertMyDocuments.lnk")
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"C:\Users\Alfa\.gemini\antigravity\scratch\docshield-converter\launch_convertmydocuments.vbs`""
$Shortcut.WorkingDirectory = "C:\Users\Alfa\.gemini\antigravity\scratch\docshield-converter"
$Shortcut.Description = "ConvertMyDocuments v1.1.0 - Zero-Leakage Offline Document and OCR Suite"
$Shortcut.IconLocation = "C:\Users\Alfa\.gemini\antigravity\scratch\docshield-converter\app_icon.ico,0"
$Shortcut.Save()
Write-Host "ConvertMyDocuments shortcut created successfully on Desktop!"
