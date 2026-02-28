@echo off
:: führe Skript aus
call python "%~dp0analyse_erfassung.py"
:: Zeige Abschlussnachricht
echo msgbox "Die Verarbeitung ist Abgeschlossen.", vbInformation, "Programm ende" > %temp%\meldung2.vbs
if exist %temp%\meldung2.vbs (
	%temp%\meldung2.vbs
	del %temp%\meldung2.vbs
)
:: Beende alles
deactivate
::wenn deactivate nicht funktioniert
endlocal
:: Console schließen
exit