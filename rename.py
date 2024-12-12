"""
    @Author: Patrick Peters
    @Date: 11.12.2024
    @Main: Ziel ist es die Dateien eines Ordners, die bereist numerisch o.Ä. sortierbar sind mit einem Datum und Zeitstempel auszustadtten, damit das Folgeprogamm die Dateien mergen kann.
"""
from tqdm import tqdm
import os
from moviepy import VideoFileClip
#import moviepy
from datetime import datetime, timedelta

# path = r"D:\OpenTrafic\2024-10_Bochum_Langendreer\Überweg"
# video = r"GP016488_2023-04-26_06-56-30.MP4"
# times='2023-04-26_06-56-30'
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
    input_string = input("Gib das Datum und die Uhrzeit des ersten Videos im Format 'YYYY-MM-DD HH-MM-SS' ein. Bei keiner Eingabe wird 1970 angenommen: ")
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

def rename_files_with_extensions(directory, datum_uhrzeit):
    extensions = [".mp4", ".MP4"]
    v_len=0
    anz=0
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
            new_file = os.path.join(directory, file)
            # Videozeit addieren
            v_len += get_video_len_ffprobe(file_path)
            # Ausführen
            try:
                os.rename(file_path, new_file)
            except FileNotFoundError:
                print(f"Die Datei '{file_path}' wurde nicht gefunden.")
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")
            anz+=1
    print(f"Im schnitt ist ein Video {v_len/anz} sek lang.")

def main():
    target_directory = abfrage_path()
    zeit = abfrage_zeit()
    isSure = input('Sind die Eingaben korrekt? (y/n): ').lower().strip()
    if isSure == 'y':
        rename_files_with_extensions(target_directory, zeit)

if __name__ == __name__:
    main()
