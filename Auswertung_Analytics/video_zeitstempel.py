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
from py import process
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

def make_video_overlay(input_path:str, output_path:str, time:int) -> None:
    """
    Erzeugt einen Zeitsempel in der Ecke des Videos. 
    Der Inputpath darf dem Outputpath nicht gleichen.
    """
    # ffmpeg -i input.mp4 -vf drawtext="fontfile=C\\:/Windows/Fonts/arial.ttf:text=%{pts\\:gmtime\\:1754565600}:x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5" -codec:a copy output.mp4
    font_path = "C\\:/Windows/Fonts/arial.ttf"

    drawtext_filter = (
        f'drawtext=fontfile=\'{font_path}\':'
        f"text=\'%{{pts\\:localtime\\:{time}}}\':"
        'x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5'
    )
    command = f'ffmpeg -y -i "{input_path}" -vf {drawtext_filter} -preset ultrafast -f mp4 -codec:a copy "{output_path}"'

    # Führe den Befehl aus
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)
    # process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE, )
    # process.wait()

def one_video(directory:str, files:list, datum_uhrzeit:datetime, extensions:list) -> str:
    """
        Erstellt eine .txt über alle Videos in einem Ordner && erstellt ein einzelnes Video aus den Splitern.
    """
    file_zsm = os.path.join(directory, 'zsm.txt')
    with open(file_zsm,'w', encoding="UTF-8") as zsm:
        for file in tqdm(files, position=1):
            pre, ext = os.path.splitext(file)
            if ext.lower() in extensions and pre.split('_') [0] != 't': # Prüfe auf mp4 Video Datei -> True
                zsm.write("file \'")
                zsm.write(os.path.join(directory, file).replace("\\", "/"))
                zsm.write("\'\n")

    file_output = (os.path.join(directory, f"fullvideo_{datum_uhrzeit.strftime('%Y-%m-%d_%H-%M-%S')}.mp4")).replace("\\", "/")

    command = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_zsm, "-c", "copy", file_output]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    logging.debug(command)# zeigt den kompletten Befehl
    logging.info(process.stdout) # zeigt ffmpeg-Ausgabe
    logging.warning(process.stderr) # zeigt ffmpeg-Fehlermeldungen

    return file_output

def einlesen(directory, datum_uhrzeit):
    # zuweisungen
    extensions = [".mp4", ".MP4"]
    v_len=anz=0
    datum_uhrzeit = datetime.strptime(datum_uhrzeit, '%d-%m-%Y %H-%M-%S')
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()

    # erzeugt ein duchgehendes Video && setzt einen Zeitstempel an das Video
    file_zsm = one_video(directory, files, datum_uhrzeit, extensions)
    make_video_overlay(file_zsm, file_zsm.strip('.mp4')+'_timestamp.mp4', int(datum_uhrzeit.timestamp()))

    #
    for file in tqdm(files, position=1): # für jede Datei im Ordner
        pre, ext = os.path.splitext(file)
        if ext.lower() in extensions and pre.split('_') [0] != 't': # Prüfe auf mp4 Video Datei -> True
            file_path = os.path.join(directory, file)
            out_file = os.path.join(directory, 't_'+file)
            
            if datum_uhrzeit is not False: # wenn Datei mit Zeit versehen werden soll 
                file = file.strip(ext)
                file = file.split('_')[0]
                neue_zeit = datum_uhrzeit + timedelta(seconds=v_len)
                datum_unix = int(neue_zeit.timestamp())

                file = file + f"_{neue_zeit.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
            
            # Video mit Timestamp versehen
            # make_video_overlay(file_path, out_file, datum_unix)
            
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
            
            # Videozeit addieren
            v_len += get_video_len_ffprobe(file_path)



    # Berechnung der Videozeit im Durchschnitt
    duration = round(v_len / anz, 0).as_integer_ratio()[0]
    logging.info(f"Im schnitt ist ein Video {duration} sek lang.")
    
    return directory, duration

def main(): 
    # Hauptablaufplan
    target, log_path = abfrage_path() # D:\Erhebungen\2025-07 Rheinbahn Düsseldorf\Video\video3.csv # D:\Erhebungen\CPM\video.csv
    logging.basicConfig(
        filename=log_path+'_logdatei.log',   # Pfad zur Logdatei
        filemode='a',                    # 'a' = anhängen, 'w' = überschreiben
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO               # Log-Level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    )
    logging.info('Programm gestartet')

# Vorlauf % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
    for idx, quellTarget in tqdm(target.iterrows(),position=0,leave=True):
        logging.info(f'Durchlauf {idx+1} von {len(target)}')

# Rename % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - % - %
        logging.info(f"Starting Rename: {datetime.now()}")
        einlesen(directory=quellTarget['pfad'], datum_uhrzeit=quellTarget['zeit'])




if __name__ == "__main__":
    main()