@echo off
:: Zeige Nachricht
echo msgbox "Bitte Meldungen in der Console bearbeiten", vbInformation, "Programm start" > %temp%\meldung1.vbs
if exist %temp%\meldung1.vbs (
	%temp%\meldung1.vbs
	del %temp%\meldung1.vbs
)
:: Setze Umgebung
setlocal
if not exist "%~dp0\OTVision" (
    echo Verzeichnis "%~dp0\OTVision" wurde nicht gefunden.
    exit /b
)
cd %~dp0\OTVision
echo start OTVision
:: Aktiviere virtuelles Py-Umfeld
if not exist "venv\Scripts\activate.bat" (
    echo Virtuelles Python-Umfeld nicht gefunden.
    exit /b
)
call venv\Scripts\activate
:: führe Skript aus
call python rename.py 
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