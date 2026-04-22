$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath

# Path to the VBS file
$vbsPath = Join-Path $scriptDir "run.vbs"

# Desktop path
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Batch File Renamer.lnk"

# Create the shortcut
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)

$shortcut.TargetPath = $vbsPath
$shortcut.WorkingDirectory = $scriptDir
$shortcut.Description = "Batch File Renamer - Web Interface"
$shortcut.IconLocation = "C:\Windows\System32\shell32.dll,13"  # Use a folder icon

# Save the shortcut
$shortcut.Save()

Write-Host "Shortcut created successfully!"
Write-Host "Location: $shortcutPath"
Write-Host ""
Write-Host "You can now double-click 'Batch File Renamer' on your desktop to launch the app!"
