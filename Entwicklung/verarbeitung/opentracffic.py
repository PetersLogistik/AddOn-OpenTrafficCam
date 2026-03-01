# -*- coding: utf-8 -*-
import os, sys
import subprocess
import platform
from pathlib import Path

def start_otc(detect:bool, directory:str, durination:int, modell:str, conf_value:float, iou_value:float, track:bool):
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
    if not python_executable.exists():
        sys.exit(1)

    if detect:
        if durination > 0: # Ohne Zeitangabe
            command = [
                str(python_executable),
                "detect.py",
                "-p", str(directory),
                "-w", f"{modell}.pt",
                "--conf", str(conf_value),
                "--iou", str(iou_value)
            ]
        else: # Mit Zeitangabe
            command = [
                str(python_executable),
                "detect.py",
                "-p", str(directory),
                "--expected-duration", str(durination),
                "-w", f"{modell}.pt",
                "--conf", str(conf_value),
                "--iou", str(iou_value) 
            ]

        subprocess.run(command, shell=True, text=True)
        # subprocess.Popen( ["cmd", "/k", str(command)], cwd=python_executable, creationflags=subprocess.CREATE_NEW_CONSOLE )

    if track:
        command = f'python track.py -p "{directory}"'
        subprocess.run(command, shell=True, text=True)
        # subprocess.Popen(
        #     ["cmd", "/k", str(command)],
        #     # cwd=python_executable,
        #     creationflags=subprocess.CREATE_NEW_CONSOLE
        # )

def short_ota():
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
    pfad = r"D:\Erhebungen\2026-02 Düsseldorf Rheinbahn\cam1"
    duri = 900
    start_otc(True, pfad, duri, "yolo11m", 0.25, 0.45 , True)