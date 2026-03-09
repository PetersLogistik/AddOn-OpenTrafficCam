# -*- coding: utf-8 -*-
import os, sys, shutil
import subprocess
from pathlib import Path

def check_otc_installed():
    """Prüft, ob otc installiert ist und gibt die Version zurück."""
    try:
        # Prüfen ob otc im PATH ist
        otc_path = shutil.which("OT_PATH")
        if not otc_path:
            return False, "otc nicht im PATH gefunden"
        
        # Version abrufen (angepasst an otc)
        result = subprocess.run(
            [otc_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version_line = result.stderr.split('\n')[0]
            return True, version_line
        else:
            return False, f"Fehler beim Ausführen: {result.stderr}"
            
    except FileNotFoundError:
        return False, "otc-Executable nicht gefunden"
    except subprocess.TimeoutExpired:
        return False, "otc-Aufruf hat zu lange gedauert"
    except Exception as e:
        return False, f"Unerwarteter Fehler: {str(e)}"
    
def start_otvision(detect:bool, directory:str, durination:int, modell:str, conf_value:float, iou_value:float, track:bool):
    # OT_PATH aus Umgebungsvariable holen
    ot_path = os.getenv("OT_PATH")
    if not ot_path:
        sys.exit(1)

    ot_vision_path = Path(ot_path) / "OTVision"

    # Prüfen ob Verzeichnis existiert
    if not ot_vision_path.exists():
        sys.exit(1)

    os.chdir(ot_vision_path)

    # Prüfen ob virtuelles Environment existiert
    python_executable = ot_vision_path / ".venv" / "Scripts" / "python.exe"
    # python_executable = Path(os.path.abspath(os.path.join(ot_vision_path, ".venv", "Scripts", "activate.bat")))
    if not python_executable.exists():
        print(f"Python-Exe nicht gefunden: {python_executable}")
        sys.exit(1)
    
    returncode = 0
    
    if detect:
        if durination > 0: # Ohne Zeitangabe
            command = [
                str(python_executable),
                "detect.py",
                "-p", os.path.abspath(directory),
                "-w", f"{modell}.pt",
                "--conf", str(conf_value),
                "--iou", str(iou_value)
            ]
        else: # Mit Zeitangabe
            command = [
                str(python_executable),
                "detect.py",
                "-p", os.path.abspath(directory),
                "--expected-duration", str(durination),
                "-w", f"{modell}.pt",
                "--conf", str(conf_value),
                "--iou", str(iou_value) 
            ]

        result  = subprocess.run(command, shell=True, text=True)
        print(result.stdout)
        print(result.stderr)
        print(result.returncode)
        returncode = result.returncode
        # subprozess(command, ot_vision_path)

    if track & returncode == 0:
        command = [
            str(python_executable),
            "track.py",
            "-p", os.path.abspath(directory)
        ]
        result  = subprocess.run(command, shell=True, text=True)
        print(result.stdout)
        print(result.stderr)
        print(result.returncode)
        # subprozess(command, ot_vision_path)
        
def subprozess(command, ot_vision_path):
    subprocess.Popen(
            command,
            cwd=ot_vision_path,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    
def start_otanalytics():
    # Absoluter Pfad zum aktuellen Python-Skript
    script_dir = Path(__file__).parent

    # Pfad zur CMD-Datei relativ zum Skript
    cmd_file = script_dir / "startOTAnalytics.cmd"

    # Neue Konsole starten
    subprocess.Popen(
        ["cmd", "/k", str(cmd_file)],  # /k = Konsole bleibt offen
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
if __name__ == "__main__":
    pass