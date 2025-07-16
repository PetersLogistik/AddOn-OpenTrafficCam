"""
    @Author: Patrick Peters
    @Date: 04.02.2025
    @Main: Ziel dieses Skipts ist es den Ablauf des OTC und die anderen Prozessschritte gebündelt und übersichtlich darzustellen.
    @Version: 1.0
"""
import os
import json
import logging
import subprocess
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta

# Get the path from the environment variable
config_path = os.getenv("OT_PATH") # Abfrage nicht notwendig, da CMD bereits abfragt

def abfrage_path():
    # Fragt nach dem zubearbeitendem Ordner
    isInput = True
    target_directory = '%'
    
    while isInput != False:
        path = input(f"Gib der Pfad der CSV-Datei ein: ").strip()
        try:
            if path == "local":
                target_directory = os.path.dirname(__file__)
            else:
                target_directory = os.path.dirname(path+'\\')
            print(f"Eingegebener Pfad: {target_directory}") 
        except Exception as e:
            print(f"Ein Fehler (File) ist aufgetreten: {e}")
        finally:
            isInput = False
    
    pfade = pd.read_csv(target_directory, sep=',', encoding="utf-8", header=0)
    
    return pfade, target_directory.strip('.csv')

def get_video_len_ffprobe(video_path):
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = json.loads(result.stdout)

    return float(info['format']['duration'])

def make_video_overlay(video_path, times=1690899780):
    command = [""" ffmpeg -i """+ video_path
        +""" -vf drawtext="fontfile=C\\:/Windows/Fonts/arial.ttf:text='%{pts\:localtime\:"""+ times
        +"""\:%H\\\\\:%M\\\\\:%S}':fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:x=10:y=10" -codec:a """]

    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = json.loads(result.stdout)

def einlesen(directory, datum_uhrzeit):
    # zuweisungen
    extensions = [".mp4", ".MP4"]
    v_len=0
    anz=0
    datum_uhrzeit = datetime.strptime(datum_uhrzeit, '%d-%m-%Y %H-%M-%S')
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()

    for file in tqdm(files, position=1): # für jede Datei im Ordner
        _, ext = os.path.splitext(file)
        if ext.lower() in extensions: # Prüfe auf mp4 Video Datei -> True
            file_path = os.path.join(directory, file)
            
            if datum_uhrzeit is not False: # wenn Datei mit Zeit versehen werden soll 
                file = file.strip(ext)
                file = file.split('_')[0]
                neue_zeit = datum_uhrzeit + timedelta(seconds=v_len)
                file = file + f"_{neue_zeit.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
            
            # Videozeit addieren
            v_len += get_video_len_ffprobe(file_path)
            
            # rename
            # Einfache Umbenennung im gegebenen Ordner
            new_file = os.path.join(directory, file)
            try:
                os.rename(file_path, new_file)
            except FileNotFoundError:
                logging.warning(f"Die Datei '{file_path}' wurde nicht gefunden.")
            except Exception as e:
                logging.warning(f"Ein Fehler (File) ist aufgetreten: {e}")
            anz+=1

    # Berechnung der Videozeit im Durchschnitt
    duration = round(v_len / anz, 0).as_integer_ratio()[0]
    logging.info(f"Im schnitt ist ein Video {duration} sek lang.")
    
    return directory, duration

def main(): 
    # Hauptablaufplan
    target, log_path = abfrage_path() # D:\Erhebungen\07-2025 Rheinbahn Düsseldorf\Video\video.csv
    logging.basicConfig(
        filename=log_path+'_logdatei.log',   # Pfad zur Logdatei
        filemode='a',                    # 'a' = anhängen, 'w' = überschreiben
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO               # Log-Level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    )
    logging.info('Programm gestartet')

# Vorlauf % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
    for idx, quellTarget in tqdm(target.iterrows(),position=0):
        logging.info(f'Durchlauf {idx+1} von {len(target)}')

# Rename % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
        logging.info(f"Starting Rename: {datetime.now()}")
        einlesen(directory=quellTarget['pfad'], datum_uhrzeit=quellTarget['zeit'])




if __name__ == "__main__":
    main()