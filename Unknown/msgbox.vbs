' Display first message box
Dim result
result = MsgBox("Do you want to play Flappy Bird?", vbYesNo + vbQuestion, "Are you sure?")
If result = vbNo Then
    WScript.Echo "Exiting the application."
    WScript.Quit
End If

' Execute Command 1 here
Dim message, title
message = "Loading ..."
title = "48% ..."

MsgBox message, vbInformation, title


' Display second message box
result = MsgBox("Are you sure?", vbYesNo + vbQuestion, "Continue?")
If result = vbNo Then
    WScript.Echo "Exiting the application."
    WScript.Quit
End If

' Execute Command 2 here
Dim message2, title2
message2 = "Loading into Flappy Bird ;) ..."
title2 = "97% ..."
MsgBox message, vbInformation, title2

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd.exe /c ""scare.bat""", 0, False
