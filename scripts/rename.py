"""
    @Author: Patrick Peters
    @Date: 11.12.2024
    @Main: Ziel ist es die Dateien eines Ordners, die bereist numerisch o.Ä. sortierbar sind mit einem Datum und Zeitstempel auszustadtten, damit das Folgeprogamm die Dateien mergen kann.
    @Version: 3.5
"""
from tqdm import tqdm
import os
import subprocess
import json
from datetime import datetime, timedelta

# Get the path from the environment variable
config_path = os.getenv("OT_PATH") # Abfrage nicht notwendig, da CMD bereits abfragt

def abfrage_zeit(isTest = False):
    # Eingabe des Datums und der Uhrzeit
    if isTest == False:
        input_string = input("Gib das Datum und die Uhrzeit des ersten Videos ein. Auchte auf das Format 'YYYY-MM-DD HH-MM-SS'. Bei keiner Eingabe (Enter) wird 1970-01-01 00-00-00 angenommen: ")
    else:
        input_string = "2025-02-24 10-00-00"
    if input_string != "":
        try:
            # Umwandlung des Eingabestrings in ein datetime-Objekt
            datetime.strptime
            datum_uhrzeit = datetime.strptime(input_string, '%Y-%m-%d %H-%M-%S')
        except ValueError:
            print("Das eingegebene Format ist ungültig. Bitte verwende das Format 'YYYY-MM-DD HH-MM-SS'.")
            abfrage_zeit()
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

def rescale_files(directory, file, file_path, zielDirectory):
    # Ordner ertstellen
    if directory == zielDirectory:
        working_path = os.path.join(directory, r"scale_videos")
        try:
                os.mkdir(working_path)
        except FileExistsError:
            pass
        except Exception as e:
            print(f"Ein Fehler (Ordner) ist aufgetreten: {e}")
        # Pfadänderung zum Ordner
        new_file = os.path.join(directory, r'scale_videos', file)
    else:
        working_path = zielDirectory
        new_file = os.path.join(zielDirectory, file)
    # Zusatz Comand öffnen und ffmpeg ausführen
    comand = [
        "ffmpeg", 
        "-i", file_path, 
        "-s", "800x600", 
        "-c:a", "copy", 
        new_file
    ] 
    comand = f'ffmpeg -i "{file_path}" -s 800x600 -c:a copy "{new_file}" 2>&1'
    comander = f'start /wait cmd /k "{comand} && exit"' # mit /c -automatisches Schließen /k -offen halten bis manuel geschlossen. /b führt den Befehl in der eigenen Shell aus.
    try:
        process = subprocess.Popen(comander, shell=True) 
        process.wait()
    except Exception as e:
        print(f"Ein Fehler ist (in Scale) aufgetreten: {e}, \n {comander}") 
    return working_path

def rename(directory, new_file_name, old_file_path):
    # Einfache Umbenennung im gegebenen Ordner
    new_file = os.path.join(directory, new_file_name)
    try:
        os.rename(old_file_path, new_file)
    except FileNotFoundError:
        print(f"Die Datei '{old_file_path}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler (File) ist aufgetreten: {e}")
    return directory

def einlesen(directory, zielDirectory, datum_uhrzeit = False, rescale = 'n', low = False):
    # zuweisungen
    extensions = [".mp4", ".MP4"]
    v_len=0
    anz=0
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()

    for file in tqdm(files): # für jede Datei im Ordner
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
            
            # Ausführen
            if rescale == 'y' and low is False: # mit rescale
                working_path = rescale_files(directory, file, file_path, zielDirectory)
            elif rescale == 'n' and low is False: # ohne scale
                working_path = rename(zielDirectory, file, file_path)
            else: # wenn Testdatei
                working_path = zielDirectory
            anz+=1
    # Berechnung der Videozeit im Durchschnitt
    duration = round(v_len / anz, 0).as_integer_ratio()[0]
    print(f"\n Im schnitt ist ein Video {duration} sek lang.", end='\n\n')
    return working_path, duration

def abfrage_path(target='Quellordner'):
    # Fragt nach dem zubearbeitendem Ordner
    isInput = True
    target_directory = '%'
    while isInput != False:
        path = input(f"Gib den {target} ein: ").strip()
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
    return target_directory

def abfragen():
    # Nutzerabfrage nach Ablaufwusch.
    target = []
    newTarget = []
    isMore = 'y'
    isRename = input('Soll den die Videos umbenannt werden? (y/n): ').lower().strip()
    if isRename != 't':
        isRescale = input('Sollen die Videos auf 800x600px reduziert werden? (y/n): ').lower().strip()
        isDetect = input('Soll Detect anschließend gestartet werden? (y/n): ').lower().strip()
        isTrack = input('Soll Track nach dem durchlauf gestartet werden? (y/n): ').lower().strip()
        isNewTarget = input('Sollen die Videos in einem anderem Ordner abgelegt werden? (y/n): ').lower().strip()
        while isMore != 'n':
            target.append(abfrage_path())
            if isNewTarget != 'n':
                newTarget.append(abfrage_path('Zielordner'))
            else: 
                newTarget = False
            isMore = input('Sollen weitere Ordner mit Videos eingegeben werden? (y/n): ').lower().strip()
        return target, isRename, isRescale, isDetect, isTrack, newTarget, False
    else:
        target.append(config_path + '\\' + 'TestVideo')
        return target, 'y', 'y', 'y', 'y', False, True

if __name__ == "__main__":
    pass