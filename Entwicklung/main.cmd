::@echo off
:: führe Skript aus
call python "%~dp0gui_helper.py"
:: Beende alles
deactivate
::wenn deactivate nicht funktioniert
endlocal
:: Console schließen
exit