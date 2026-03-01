# -*- coding: utf-8 -*-
import subprocess

def start_otc(detect:bool, directory:str, durination:str, modell:str, conf_value:str, iou_value:str, track:bool) -> None:
    """
    
    """
    command = [
        "set PATH_TO_OT=%OT_PATH%",
        "setlocal",
        'cd "%PATH_TO_OT%\OTVision"',
        "echo start OTVision",
        "call .venv\Scripts\activate",
        "deactivate",
        "endlocal",
        "exit"
    ]

    if detect is True:
        commandline = start_detect(directory, durination, modell, conf_value, iou_value)
        command.insert(6, commandline)

    if track is True:
        commandline = start_track(directory)
        i = 6
        if detect:
            i += 1
        command.insert(i, commandline)

    try:
        result = subprocess.run(command, shell=True, text=True)
    except Exception as e:
        print(f"Ein Fehler (File) ist aufgetreten: {e}")
    else:
        print(result.stdout)
        print(result.stderr)
        print(result.returncode) 
    
def start_detect(directory:str, durination:int, modell:str, conf_value:float, iou_value:float) -> None:
    """
        Hierdurch wird Detect gestartet.
        # Standard:  YOLOv8s, Konfidenzschwelle 0.25, IoU-Schwelle 0.45
        # version 2: YOLOv8m, Konfidenzschwelle 0.1, IoU-Schwelle 0.6
        # version 3: YOLOv11m, Konfidenzschwelle 0.1, IoU-Schwelle 0.6
    """
    if durination > 0:
        command = f'python detect.py -p "{directory}" --expected-duration "{durination}" -w {modell}.pt --conf {conf_value} --iou {iou_value}' 
    else:
        command = f'python detect.py -p "{directory}" -w {modell}.pt --conf {conf_value} --iou {iou_value}'
    
    return command


def start_track(directory:str) -> None:
    """
        Hierdurch wird Track gestartet.
    """
    command = f'python track.py -p "{directory}"'
    return command
