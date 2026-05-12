Option Explicit

Dim shell
Dim repoRoot
Dim wrapperPath
Dim command
Dim exitCode

Set shell = CreateObject("WScript.Shell")

repoRoot = "C:\Users\equin\Documents\institutional-ea"
wrapperPath = repoRoot & "\scripts\run_h024_read_only_vps_observer_scheduled.ps1"

shell.CurrentDirectory = repoRoot

command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File " & Chr(34) & wrapperPath & Chr(34)

exitCode = shell.Run(command, 0, True)

WScript.Quit exitCode
