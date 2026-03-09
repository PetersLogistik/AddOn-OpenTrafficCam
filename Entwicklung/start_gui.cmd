::@echo off

:: Aktiviere virtuelles Py-Umfeld
if not exist ".env\Scripts\activate.bat" (
    echo Virtuelles Python-Umfeld nicht gefunden.
    python -m venv .env
    call .env\Scripts\activate
    python.exe -m pip install --upgrade pip
    pip install -r guiBueffee/requirements.txt --no-cache-dir
    
    echo "Installation abgeschlossen"
)

call .env\Scripts\activate.bat
:: führe Skript aus
call python "%~dp0guiBueffee/gui_helper.py"
:: Beende alles
deactivate
::wenn deactivate nicht funktioniert
endlocal
:: Console schließen
::exit