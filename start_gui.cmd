@echo off
setlocal

:: Aktiviere virtuelles Py-Umfeld
if not exist ".env\Scripts\activate.bat" (
    echo Virtuelles Python-Umfeld nicht gefunden. Installation wird gestartet...
    python -m venv .env
    
    :: Aktiviere das neue Umfeld
    call .env\Scripts\activate.bat
    
    :: Pip upgraden und Abhängigkeiten installieren
    python -m pip install --upgrade pip
    python -m pip install -r guiBueffee/requirements.txt --no-cache-dir
    
    echo Installation abgeschlossen.
) else (
    echo Virtuelles Python-Umfeld bereits vorhanden.
)

:: Aktiviere das Umfeld (falls es schon existierte oder um sicherzugehen)
call .env\Scripts\activate

:: Führe Skript aus (mit absolutem Pfad zum Skript-Ordner)
call python "%~dp0guiBueffee\gui_helper.py" > error.log 2>&1

:: Beende virtuelles Umfeld
deactivate

:: Warte kurz, damit man Fehler sehen kann (optional)
pause

::endlocal
exit