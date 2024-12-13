"""
    @Author: Patrick Peters
    @Date: 11.12.2024
    @Main: Ziel ist es die Dateien eines Ordners, die bereist numerisch o.Ä. sortierbar sind mit einem Datum und Zeitstempel auszustadtten, damit das Folgeprogamm die Dateien mergen kann.
"""
from tqdm import tqdm
import os
import subprocess
import json
from datetime import datetime, timedelta
import requests

def abfrage_path():
    path = input("Gib den Zielordner ein: ").strip()
    if path == "":
        target_directory = os.path.dirname(__file__)
    else:
        target_directory = os.path.dirname(path+'\\')
    print(f"Eingegebener Pfad: {target_directory}") 
    return target_directory

def abfrage_zeit():
    # Eingabe des Datums und der Uhrzeit
    input_string = input("Gib das Datum und die Uhrzeit des ersten Videos im Format 'YYYY-MM-DD HH-MM-SS' ein. Bei keiner Eingabe wird 1970-01-01 00:00:00 angenommen: ")
    if input_string != "":
        try:
            # Umwandlung des Eingabestrings in ein datetime-Objekt
            datum_uhrzeit = datetime.strptime(input_string, '%Y-%m-%d %H-%M-%S')
        except ValueError:
            print("Das eingegebene Format ist ungültig. Bitte verwende das Format 'YYYY-MM-DD HH-MM-SS'.")
    else:
        datum_uhrzeit = datetime.strptime('1970-01-01 00-00-00', '%Y-%m-%d %H-%M-%S')

    # Ausgabe im gewünschten Format
    print("Eingegebenes Datum und Uhrzeit:")
    print(f"Datum: {datum_uhrzeit.strftime('%d.%m.%Y')}")
    print(f"Uhrzeit: {datum_uhrzeit.strftime('%H:%M:%S')}")
    return datum_uhrzeit

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


def rename_files_with_extensions(directory, datum_uhrzeit, rescale = 'n'):
    extensions = [".mp4", ".MP4"]
    v_len=0
    anz=0
    worklist = []
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()

    for file in tqdm(files):
        _, ext = os.path.splitext(file)
        if ext.lower() in extensions:
            file_path = os.path.join(directory, file)
            
            # Namen generieren
            file = file.strip(ext)
            file = file.split('_')[0]
            neue_zeit = datum_uhrzeit + timedelta(seconds=v_len)
            file = file + f"_{neue_zeit.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
            
            # Videozeit addieren
            v_len += get_video_len_ffprobe(file_path)
            
            # Ausführen
            if rescale == 'y': # mit rescale
                # Ordner ertstellen
                working_path = os.path.join(directory, r"scale_videos")
                try:
                     os.mkdir(working_path)
                except FileExistsError:
                    pass
                except Exception as e:
                    print(f"Ein Fehler (Ordner) ist aufgetreten: {e}")
                # Pfadänderung zum Ordner
                new_file = os.path.join(directory, r'scale_videos', file)
                # Zusatz Comand öffnen und ffmpeg ausführen
                command = f"ffmpeg -i {file_path} -s 800x600 -c:a copy {new_file}"
                comander = f'start /wait cmd /c "{command}"' 
                try:
                    process = subprocess.Popen(comander, shell=True) 
                    process.wait()
                except Exception as e:
                    print(f"Ein Fehler (Scale) ist aufgetreten: {e}, \n {comander}")
            else: # ohne scale
                # Einfache Umbenennung im gegebenen Ordner
                working_path = directory
                new_file = os.path.join(directory, file)
                try:
                    os.rename(file_path, new_file)
                except FileNotFoundError:
                    print(f"Die Datei '{file_path}' wurde nicht gefunden.")
                except Exception as e:
                    print(f"Ein Fehler (File) ist aufgetreten: {e}")
            anz+=1
    # Berechnung der Videozeit im Durchschnitt
    duration = round(v_len / anz, 0).as_integer_ratio()[0]
    print(f"Im schnitt ist ein Video {duration} sek lang.")
    return working_path, duration

def tsenden(nachricht = 'Sollte was senden, weiß nicht was...'):
    # die chat_id ist die aus der obigen Response
    token="7758414756:AAE-1IXr8StbPOLpVL0IgrDJOFvbsi7ukac"
    params = {"chat_id":"7464651487", "text":nachricht}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, params=params)

def main():
    target_directory = abfrage_path()
    zeit = abfrage_zeit()
    rescale = input('Sollen die Videos auf 800x600px reduziert werden? (y/n): ').lower().strip()
    isSure = input('Sind die Eingaben korrekt? (y/n): ').lower().strip()
    isDetect = input('Soll Detect anschließend gestartet werden? (y/n): ').lower().strip()
    isTrack = input('Soll Track nach dem durchlauf gestartet werden? (y/n): ').lower().strip()
    if isSure == 'y':
        working, duration = rename_files_with_extensions(target_directory, zeit, rescale)
    if isDetect == 'y':
        command = f'python detect.py -p "{working}" --expected_duration "{duration}"'
        try:
           subprocess.run(command, shell=True)
        except Exception as e:
           tsenden(f"Ein Fehler (File) ist aufgetreten: {e}")
    if isTrack == 'y':
        command = f'python track.py -p "{working}"'
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
           tsenden(f"Ein Fehler (File) ist aufgetreten: {e}")
        
if __name__ == __name__:
    main()
