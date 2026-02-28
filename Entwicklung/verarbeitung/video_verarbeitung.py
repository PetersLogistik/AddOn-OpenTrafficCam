# -*- coding: utf-8 -*-
import os, re
import subprocess
import json
from datetime import datetime, timedelta

def extrahiere_datum(dateiname):
        """
            Diese Funktion ermittelt bei den Videos eine Uhrzeit und gibt diese zurück.
        """
        # Muster für "video_2026-02-24_07-00-27.mp4"
        muster = r"_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})"
        
        treffer = re.search(muster, dateiname)
        if treffer:
            jahr, monat, tag, stunde, minute, sekunde = treffer.groups()
            datum = datetime(int(jahr), int(monat), int(tag), int(stunde), int(minute), int(sekunde))
            return datum
        try:
            timestamp = os.path.getmtime(dateiname)
            return datetime.fromtimestamp(timestamp)
        except:
            return "YYYY-mm-dd HH-MM-SS"

def timeparser(date_string: str, test=False) -> datetime:
    """
    Versucht, das Datum mit jedem Format aus der Liste zu parsen.
    Gibt das erste erfolgreiche datetime‑Objekt zurück.
    Falls kein Format passt, wird ein ValueError ausgelöst.
    """
    formats = [
        "%Y-%m-%d %H-%M-%S",
        "%Y-%m-%d %H-%M-%S.",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.",
        "%Y-%m-%d %H.%M.%S",
        "%Y-%m-%d %H.%M.%S.",
        
        "%Y.%m.%d %H-%M-%S",
        "%Y.%m.%d %H-%M-%S.",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M:%S.",
        "%Y.%m.%d %H.%M.%S",
        "%Y.%m.%d %H.%M.%S.",

        "%Y-%m-%d_%H-%M-%S",
        "%Y-%m-%d_%H-%M-%S.",
        "%Y-%m-%d_%H:%M:%S",
        "%Y-%m-%d_%H:%M:%S.",
        "%Y-%m-%d_%H.%M.%S",
        "%Y-%m-%d_%H.%M.%S.",
        
        "%Y.%m.%d_%H-%M-%S",
        "%Y.%m.%d_%H-%M-%S.",
        "%Y.%m.%d_%H:%M:%S",
        "%Y.%m.%d_%H:%M:%S.",
        "%Y.%m.%d_%H.%M.%S",
        "%Y.%m.%d_%H.%M.%S.",
    ]
    for fmt in formats:
        try:
            datum_uhrzeit = datetime.strptime(date_string, fmt)
            if test:
                return True, datum_uhrzeit.strftime('%Y-%m-%d %H-%M-%S')
            return datum_uhrzeit
        except ValueError:
            continue

    # Kein Format hat funktioniert
    raise ValueError(f"Keines der angegebenen Formate hat '{date_string}' erkannt.")
    
def get_next_starttime(start_zeit, video_pfad) -> str:
    """
        Gibt die neue Startzeit für das folgende Video zurück.
    """
    begin_zeit = timeparser(start_zeit)
    video_len = get_video_len_ffprobe(video_pfad)
    begin_zeit += timedelta(seconds=video_len)

    return begin_zeit.strftime('%Y-%m-%d %H-%M-%S')

def get_video_len_ffprobe(video_path):
    """
        Gibt die Zeitlänge eines Videos zurück.
    """
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        f"{video_path}"
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = json.loads(result.stdout)
    return float(info['format']['duration'])        

def datei_name_anpassen(file_path, zeitstempel, pre="") -> str:
    datum_uhrzeit = timeparser(zeitstempel)
    
    path, _ = os.path.splitext(file_path)
    file = path.split('\\')[-1]
    path = path.strip(file)
    file = file.split('_')[0]
    
    newfilename = path + pre + file + f"_{datum_uhrzeit.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    return newfilename

def rename_Datei(file_path, zeitstempel) -> None:
    """
        Einfache Umbenennung im gegebenen Ordner
    """
    new_filename = datei_name_anpassen(file_path, zeitstempel)

    try:
        os.rename(file_path, new_filename)
    except FileNotFoundError:
        return f"Der Pfad '{file_path}' wurde nicht gefunden."
    except Exception as e:
        return f"Ein Fehler (File) ist aufgetreten: {e}"
    else:
        return None

def make_video_overlay(input_path:str, startzeit:str) -> None:
    """
    Erzeugt einen Zeitsempel in der Ecke des Videos. 
    Der Inputpath darf dem Outputpath nicht gleichen.
    Zeit muss als string eingegeben werden.
    """
    time = timeparser(startzeit).timestamp()

    # ffmpeg -i input.mp4 -vf drawtext="fontfile=C\\:/Windows/Fonts/arial.ttf:text=%{pts\\:gmtime\\:1754565600}:x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5" -codec:a copy output.mp4
    font_path = "C\\:/Windows/Fonts/arial.ttf"

    drawtext_filter = (
        f'drawtext=fontfile=\'{font_path}\':'
        f"text=\'%{{pts\\:localtime\\:{time}}}\':"
        'x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5'
    )
    output_path = input_path.strip('.mp4')+'_timestamp.mp4'
    command = f'ffmpeg -y -i "{input_path}" -vf {drawtext_filter} -preset ultrafast -f mp4 -codec:a copy "{output_path}"'

    # Führe den Befehl aus
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)
    # process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE, )
    # process.wait()

    if os.path.exists(input_path): # Entfernt die Datei, wenn sie vorhanden ist.
        os.remove(input_path)

def one_video(directory:str, time:str) -> object:
    """
        Erstellt eine .txt über alle Videos in einem Ordner && erstellt ein einzelnes Video aus den Splitern.
    """
    extensions = [".mp4", ".MP4", ".avi",".mkv",".mov"]
    datum_uhrzeit = timeparser(time)
    file_output = os.path.abspath(os.path.join(directory, f"fullvideo_{datum_uhrzeit.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"))

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    file_zsm = os.path.join(directory, 'zsm.txt')
    with open(file_zsm,'w', encoding="UTF-8") as zsm:
        for file in files:
            pre, ext = os.path.splitext(file)
            if ext.lower() in extensions and pre.split('_') [0] != 't': # Prüfe auf mp4 Video Datei -> True
                zsm.write("file \'")
                zsm.write(os.path.join(directory, file).replace("\\", "/"))
                zsm.write("\'\n")

    # Startet die Shell und setzt die Splitter zusammen.
    command = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_zsm, "-c", "copy", file_output]
    # process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE, )
    process.wait()

    if os.path.exists(file_zsm): # Entfernt die Datei, wenn sie vorhanden ist.
        os.remove(file_zsm)
    
    return file_output, datum_uhrzeit.strftime('%Y-%m-%d_%H-%M-%S')

if __name__ == '__main__':
     pass