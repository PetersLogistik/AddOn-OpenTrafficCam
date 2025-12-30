@echo off
:: holt sich den Pfad zu OT
set PATH_TO_OT=%OT_PATH%
if "%OT_PATH%"=="" (
	:: Zeigt Meldung bei fehlenderm Path Pfad
    echo msgbox "Die Umgebungsvariable 'OT_PATH' ist nicht gesetzt. Bitte in Path einsetzen. \n Variable=OT_PATH & Wert=Pfad-zum-Oberordner", vbInformation, "Programm start" > %temp%\meldung1.vbs
	if exist %temp%\meldung1.vbs (
		%temp%\meldung1.vbs
		del %temp%\meldung1.vbs
	)
    exit /b 1
)
:: Setze Umgebung
setlocal
if not exist "%PATH_TO_OT%\OTVision" (
    echo Verzeichnis "%PATH_TO_OT%\OTVision" wurde nicht gefunden.
    exit /b
)
cd "%PATH_TO_OT%\OTVision"
echo start OTVision
:: Aktiviere virtuelles Py-Umfeld
if not exist ".venv\Scripts\activate.bat" (
    echo Virtuelles Python-Umfeld nicht gefunden.
    exit /b
)
call .venv\Scripts\activate
:: führe Skript aus
call python "%~dp0conf_iou_test.py"
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