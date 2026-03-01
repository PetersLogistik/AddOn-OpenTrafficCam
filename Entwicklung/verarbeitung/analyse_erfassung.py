# -*- coding: utf-8 -*-
import os
import yaml
import pandas as pd
from .video_verarbeitung import extrahiere_datum, timeparser, get_next_starttime, dateipfad_anpassen, one_video, make_video_overlay, get_video_len_ffprobe

def get_standard_values(value:str=None) -> object:
    """
        Reading a config file
    """
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "basiswerte.yaml")
    with open(file, "r") as file:
        werte = yaml.safe_load(file)
    
    if value != None:
        return werte[f"{value}"]
    else:
        return werte 

def dateien_laden(directory:str) -> object:
    """
    """
    extensions = get_standard_values("video_extensions")
    df_videos = pd.DataFrame({ "zeit": [], "dateiname": [], "dateipfad": [] , "basispfad": []})
    
    if directory:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        files.sort()

        for file in files: # für jede Datei im Ordner
            _, ext = os.path.splitext(file)
            if ext.lower() in extensions: # Prüfe auf Video Datei -> True
                file_path = os.path.abspath(os.path.join(directory, file))
                date = str(extrahiere_datum(file))

                df_videos.loc[len(df_videos)] = [date, file, file_path, directory]   
        if len(df_videos) == 0: # Keine Vidoes
            return True, df_videos, f"Inhalt"
        return False, df_videos, None
    else: # Kein Pfad
        return True, df_videos, f"Pfad"

def convert_to_pandas(daten:list, names:list) -> object:
    """
        convertiert eine Liste in ein Dateframe
    """
    names = [x.lower() for x in names] # macht Kleinbuchstaben
    df = pd.DataFrame(daten)
    df.columns = names # Hängt die Überschriften an
    
    for idx, row in df.iterrows(): # Fügt alles in ein Zeitformat
        error, datum_uhrzeit = timeparser(row["zeit"],"str")
        if error:
            df.loc[idx]["zeit"] = None
        else:
            df.loc[idx]["zeit"] = datum_uhrzeit

    return df

def test_zeiteingabe(df_video:dict, mainpfad:dict) -> bool:
    """
        Soll feststellen, ob die Eingegebenen Uhrzeiten stimmen.
    """
    groups = df_video.groupby("basispfad")
    for idx, liste in enumerate(mainpfad,1):
        df_guppe = groups.get_group(f"{liste['pfad']}")
        times = df_guppe.iloc[0, 0]
        error, datum_uhrzeit = timeparser(times)
        if error:
            return error, idx, datum_uhrzeit
    return False, None, None

def zeiten_anpassen(df_video: pd.DataFrame, mainpfad: list[dict]) -> pd.DataFrame:
    """
    Passt die 'zeit'-Spalte basierend auf dem nächsten Videostart an.
    """
    groups = df_video.groupby("basispfad")
    for idx, liste in enumerate(mainpfad,1):
        df_guppe = groups.get_group(f"{liste['pfad']}")
        for i in range(df_guppe.index.min(), df_guppe.index.max()):
            startzeit = df_guppe.loc[i,"zeit"]
            video_pfad = df_guppe.loc[i,"dateipfad"]
            datum_uhrzeit_neu = get_next_starttime(startzeit, video_pfad)
            df_guppe.loc[i+1,"zeit"] = datum_uhrzeit_neu

        df_video.loc[df_guppe.index, 'zeit'] = df_guppe["zeit"]

    return df_video

def dateiname_anpassen(df_video: pd.DataFrame) -> None :
    for i in range(df_video.index.min(), df_video.index.max()+1):
        dateipfad_anpassen(df_video.loc[i,"dateipfad"],df_video.loc[i,"zeit"])
        
def make_onevideo(df_video: pd.DataFrame) -> None:
        """
        """
        groups = df_video.groupby("basispfad")
        for basispfad, grupppe in groups:
            zeit = grupppe.iloc[0, 0]
            one_video(basispfad, zeit)

def videozeit_in_video(df_video: pd.DataFrame) -> None:
    for idx, video in df_video.iterrows():
        path = video[2]
        zeit = video[0]
        make_video_overlay(path, zeit)

def get_durination(directory):
    """
        Misst die durchschnittliche Zeit der Videos
    """
    extensions = get_standard_values("video_extensions")
    anz = v_len = 0
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()

    for file in files: # für jede Datei im Ordner
        _, ext = os.path.splitext(file)
        if ext.lower() in extensions: # Prüfe auf mp4 Video Datei -> True
            file_path = os.path.join(directory, file) 
            # Videozeit addieren
            v_len += get_video_len_ffprobe(file_path)
            anz += 1

    return round(v_len / anz, 0).as_integer_ratio()[0]

if __name__ == "__main__":
    # print(dateien_laden(r"J:\Düsseldorf 01.07.2025 und 03.07.2025\03.07.2025\cam3\7-10.15uhr\354GOPRO"))
    pass