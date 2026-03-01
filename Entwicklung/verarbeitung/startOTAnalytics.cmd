@echo off
:: Auf bestimmte Python Version prüfen
FOR /F "tokens=* USEBACKQ" %%F IN (`python --version`) DO SET PYTHON_VERSION=%%F
echo %PYTHON_VERSION%

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
:: In Verzeichnis wechseln
setlocal
cd "%PATH_TO_OT%\OTAnalytics"
if not exist "%PATH_TO_OT%\OTAnalytics" (
    echo Verzeichnis "%PATH_TO_OT%\OTAnalytics" wurde nicht gefunden.
    exit /b
)
start_gui.cmd

:: Aktiviere virtuelles Py-Umfeld
::call .venv\Scripts\activate
::python -m OTAnalytics %*
:: Beende alles
::deactivate
:: Console schließen
exit