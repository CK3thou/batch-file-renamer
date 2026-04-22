Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
strScriptPath = WScript.ScriptFullName
strScriptDir = objFSO.GetParentFolderName(strScriptPath)

' Run the batch file with no console window
strBatchFile = objFSO.BuildPath(strScriptDir, "run.bat")

' Run the batch file silently (0 = hidden window)
objShell.Run """" & strBatchFile & """", 0, False

' Show a notification (if Windows 10+)
MsgBox "Batch File Renamer is starting..." & vbNewLine & "The web interface will open in your browser.", vbInformation, "Batch File Renamer"
