"""
    @Author: Patrick Peters
    @Date: 11.12.2024
    @Main: Ziel ist es die Dateien eines Ordners, die bereist numerisch o.Ä. sortierbar sind mit einem Datum und Zeitstempel auszustadtten, damit das Folgeprogamm die Dateien mergen kann.
    @Version: 3.0
"""
from tqdm import tqdm
import os
import subprocess
import json
from datetime import datetime, timedelta

# Get the path from the environment variable
config_path = os.getenv("OT_PATH") # Abfrage nicht notwendig, da CMD bereits abfragt

def abfrage_zeit():
    # Eingabe des Datums und der Uhrzeit
    input_string = input("Gib das Datum und die Uhrzeit des ersten Videos ein. Auchte auf das Format 'YYYY-MM-DD HH-MM-SS'. Bei keiner Eingabe (Enter) wird 1970-01-01 00:00:00 angenommen: ")
    if input_string != "":
        try:
            # Umwandlung des Eingabestrings in ein datetime-Objekt
            datetime.strptime
            datum_uhrzeit = datetime.strptime(input_string, '%Y-%m-%d %H:%M:%S')
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

def rescale_files(directory, file, file_path):
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

def rename(directory, file, file_path):
    # Einfache Umbenennung im gegebenen Ordner
    new_file = os.path.join(directory, file)
    try:
        os.rename(file_path, new_file)
    except FileNotFoundError:
        print(f"Die Datei '{file_path}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler (File) ist aufgetreten: {e}")
    return directory

def einlesen(directory, datum_uhrzeit = False, rescale = 'n', low = False):
    extensions = [".mp4", ".MP4"]
    v_len=0
    anz=0
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()

    for file in tqdm(files):
        _, ext = os.path.splitext(file)
        if ext.lower() in extensions:
            file_path = os.path.join(directory, file)
            
            if datum_uhrzeit is not False:
                # Namen generieren
                file = file.strip(ext)
                file = file.split('_')[0]
                neue_zeit = datum_uhrzeit + timedelta(seconds=v_len)
                file = file + f"_{neue_zeit.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
            
            # Videozeit addieren
            v_len += get_video_len_ffprobe(file_path)
            
            # Ausführen
            if rescale == 'y' and low is False: # mit rescale
                working_path = rescale_files(directory, file, file_path)
            elif rescale != 'y' and low is False: # ohne scale
                working_path = rename(directory, file, file_path)
            else:
                working_path = directory
            anz+=1
    # Berechnung der Videozeit im Durchschnitt
    duration = round(v_len / anz, 0).as_integer_ratio()[0]
    print(f"\n Im schnitt ist ein Video {duration} sek lang.", end='\n\n')
    return working_path, duration

def abfrage_path():
    # Fragt nach dem zubearbeitendem Ordner
    isInput = True
    target_directory = '%'
    while isInput != False:
        path = input("Gib den Zielordner ein: ").strip()
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
    isMore = 'y'
    isRename = input('Soll den die Videos umbenannt werden? (y/n): ').lower().strip()
    isRescale = input('Sollen die Videos auf 800x600px reduziert werden? (y/n): ').lower().strip()
    isDetect = input('Soll Detect anschließend gestartet werden? (y/n): ').lower().strip()
    isTrack = input('Soll Track nach dem durchlauf gestartet werden? (y/n): ').lower().strip()

    while isMore != 'n':
        target.append(abfrage_path())
        isMore = input('Sollen weitere Ordner mit Videos eingegeben werden? (y/n): ').lower().strip()
    return target, isRename, isRescale, isDetect, isTrack

def main():
    import subprocess
    import torch
    comander = f'msg * " CUDA active: {torch.cuda.is_available()}, {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Keine GPU"}"'
    subprocess.run(comander, text=True)
    
    # Hauptablaufplan
    target, isRename, isRescale, isDetect, isTrack = abfragen()
    for target_directory in tqdm(target):
        if isRescale == 'y':
            print(f"Starting Scaling: {datetime.now()}")
            zeit = abfrage_zeit()
            isSure = input(f'Sind die Eingaben für den Ordner {target_directory} korrekt? (y/n): ').lower().strip()
            if isSure == 'y': 
                target_directory, duration = einlesen(target_directory, zeit, isRescale)
        elif isRename == 'y':
            print(f"Starting Rename: {datetime.now()}")
            zeit = abfrage_zeit()
            isSure = input(f'Sind die Eingaben für den Ordner {target_directory} korrekt? (y/n): ').lower().strip()
            if isSure == 'y': 
                target_directory, duration = einlesen(target_directory, zeit)

        if isDetect == 'y':
            print(f"Starting Detect: {datetime.now()}")
            if isDetect == 'y': 
                target_directory, duration = einlesen(target_directory, low=True)
                command = f'python detect.py -p "{target_directory}" --expected_duration "{duration}"'
                try:
                    subprocess.run(command, shell=True)
                except Exception as e:
                    print(f"Ein Fehler (File) ist aufgetreten: {e}")

        if isTrack == 'y':
            print(f"Starting Track: {datetime.now()}")
            if isTrack == 'y': 
                command = f'python track.py -p "{target_directory}"'
                try:
                    subprocess.run(command, shell=True)
                except Exception as e:
                    print(f"Ein Fehler (File) ist aufgetreten: {e}")
    subprocess.run(f'msg * "Py-Programm abgeschlossen."', text=True)
        
if __name__ == "__main__":
    main()