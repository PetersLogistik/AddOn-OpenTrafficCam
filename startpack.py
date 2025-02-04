"""
    @Author: Patrick Peters
    @Date: 04.02.2025
    @Main: Ziel dieses Skipts ist es den Ablauf des OTC und die anderen Prozessschritte gebündelt und übersichtlich darzustellen.
    @Version: 1.0
"""
from tqdm import tqdm
import os
import subprocess
from datetime import datetime, timedelta
import rename as rn

# Get the path from the environment variable
config_path = os.getenv("OT_PATH") # Abfrage nicht notwendig, da CMD bereits abfragt

def main():
    # Hauptablaufplan
    target, isRename, isRescale, isDetect, isTrack, newTarget, isTest = rn.abfragen()
    zeit = False
# Vorlauf % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
    for idx, quellTarget in tqdm(enumerate(target)):
        if newTarget != False:
            zielTarget = newTarget[idx]
        else:
            zielTarget = quellTarget
# Rename & Rescale % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
        if isRescale == 'y':
            print(f"Starting Scaling: {datetime.now()}")
            if zeit == False:
                zeit = rn.abfrage_zeit(isTest)
            if isTest == True or zeit != False:
                isSure = 'y'
            else:
                isSure = input(f'Sind die Eingaben für den Ordner {quellTarget} korrekt? (y/n): ').lower().strip()
            if isSure == 'y': 
                zielTarget, duration = rn.einlesen(directory=quellTarget, datum_uhrzeit=zeit, rescale=isRescale, zielDirectory=zielTarget)
# Rename only % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
        if isRename == 'y':
            print(f"Starting Rename: {datetime.now()}")
            if zeit == False:
                zeit = rn.abfrage_zeit()
            if zeit != False:
                isSure = 'y'
            else:
                isSure = input(f'Sind die Eingaben für den Ordner {quellTarget} korrekt? (y/n): ').lower().strip()
            if isSure == 'y': 
                zielTarget, duration = rn.einlesen(directory=quellTarget, datum_uhrzeit=zeit, zielDirectory=zielTarget)

# OTC % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
    for idx, quellTarget in tqdm(enumerate(target)):
        if newTarget != False:
            zielTarget = newTarget[idx]
        else:
            zielTarget = quellTarget
# Detect % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
        if isDetect == 'y':
            print(f"Starting Detect: {datetime.now()}")
            if isDetect == 'y': 
                zielTarget, duration = rn.einlesen(quellTarget, zielTarget, low=True)
                # command = f'python detect.py -p "{target_directory}" --expected_duration "{duration}"' # standart YOLOv8s, Konfidenzschwelle 0.25, IoU-Schwelle 0.45
                # command = f'python detect.py -p "{target_directory}" --expected_duration "{duration}" -w yolov8m.pt --conf 0.1 --iou 0.6 ' # version 2: YOLOv8m, Konfidenzschwelle 0.1, IoU-Schwelle 0.6
                command = f'python detect.py -p "{zielTarget}" --expected_duration "{duration}" -w yolo11m.pt --conf 0.1 --iou 0.6 ' # version 3: YOLOv11m, Konfidenzschwelle 0.1, IoU-Schwelle 0.6
                try:
                    subprocess.run(command, shell=True)
                except Exception as e:
                    print(f"Ein Fehler (File) ist aufgetreten: {e}")
# Track % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
        if isTrack == 'y':
            print(f"Starting Track: {datetime.now()}")
            if isTrack == 'y': 
                command = f'python track.py -p "{zielTarget}"'
                try:
                    subprocess.run(command, shell=True)
                except Exception as e:
                    print(f"Ein Fehler (File) ist aufgetreten: {e}")
    subprocess.run(f'msg * "Py-Programm abgeschlossen."', text=True)
        
if __name__ == "__main__":
    main()