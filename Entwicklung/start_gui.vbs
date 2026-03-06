Set WshShell = CreateObject("WScript.Shell")
' 0 = Fenster ausblenden, True = Warten bis Skript fertig ist
WshShell.Run "start_gui.bat", 0, True
Set WshShell = Nothing