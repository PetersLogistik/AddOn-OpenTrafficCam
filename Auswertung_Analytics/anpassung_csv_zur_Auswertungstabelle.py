# UTF-8
import pandas as pd
from tqdm import tqdm
import numpy as np
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def convert(file_path, sep=',') -> None:
    df = pd.read_csv(file_path, sep=sep, header=0, encoding='utf-8')
    df['Knotenpunkt'] = '01'
    col = {'start occurrence date':'DATUM', 
           'Knotenpunkt':'KNOTENPUNKT', 
           'from section':'VON_ARM', 
           'to section':'NACH_ARM', 
           'start occurrence time':'VON_UHR', 
           'end occurrence time':'BIS_UHR'}
    df = df.rename(columns=col)
    kn = df[['DATUM', 'KNOTENPUNKT', 'VON_ARM', 'NACH_ARM', 'VON_UHR', 'BIS_UHR']]
    # kn = kn.groupby(['DATUM', 'VON_ARM', 'NACH_ARM', 'VON_UHR']).first().reset_index()
    kn = kn.drop_duplicates(['DATUM', 'VON_ARM', 'NACH_ARM', 'VON_UHR'])
    print(kn)
    kn = kn.join(pd.DataFrame({
        'PKW':0,
        'KRAD':0, 
        'RAD':0, 
        'LIEFER':0, 
        'LKW':0, 
        'LASTZUG':0, 
        'STRAB':0, 
        'BUS':0, 
        'FG':0, 
        'SONDER':0
        }, index=df.index))
    print(kn)
    for id, row in tqdm(df.iterrows()):
        # Finde den Index in kn (nach reset_index ist es 0-basiert)
        matching_rows = kn[(kn['VON_UHR'] == row['VON_UHR']) & 
                           (kn['VON_ARM'] == row['VON_ARM']) & 
                           (kn['NACH_ARM'] == row['NACH_ARM'])]
        if not matching_rows.empty:
            idx = matching_rows.index[0]  # Erster Treffer (sollte eindeutig sein nach drop_duplicates)
    # Zuweisen der Messzahlen der Erhebung den Zellen
            typ = row['classification']
            count = row['count']
            if typ == 'bicycle':
                kn.loc[idx, 'RAD'] = count
            elif typ == 'bus':
                kn.loc[idx, 'BUS'] = count
            elif typ == 'car':
                kn.loc[idx, 'PKW'] = count
            elif typ == 'motorcycle':
                kn.loc[idx, 'KRAD'] = count
            elif typ == 'person':
                kn.loc[idx, 'FG'] = count
            elif typ == 'train':
                kn.loc[idx, 'STRAB'] = count
            elif typ == 'truck':
                kn.loc[idx, 'LKW'] = count
    file = file_path.replace('.csv','_bueffeeTale.xlsx', 1)
    kn.to_excel(file, sheet_name='DB-01', index=False)

    return file

def stromliste(intervall, df):
    # Erstelle Farhzeug Liste
    strom = pd.DataFrame({
        'Fg':[np.nan]*intervall,
        'Rad':[np.nan]*intervall,
        'K-Rad': [np.nan]*intervall,
        'Pkw':[np.nan]*intervall,
        'Lfw':[np.nan]*intervall,
        'Lkw':[np.nan]*intervall,
        'Bus':[np.nan]*intervall,
        'Lz/ Sz':[np.nan]*intervall,
        'PKW-E':[np.nan]*intervall,
        'Kfz': [np.nan]*intervall,
        'SV':[np.nan]*intervall
        }, index=df.index)
    return strom

def firstpage(file, minutes=15):
    intervall = int((60/minutes)*24)
    # DataFrame für die Fahrzeugtypen-Faktoren
    vehicle_factors = pd.DataFrame({
        'Fg': ['PKW-E', 'Kfz', 'SV'],
        'Rad': [0.5, 1, np.nan],
        'K-Rad': [1, 1, np.nan],
        'Pkw': [1, 1, np.nan],
        'Lfw': [1, 1, np.nan],
        'Lkw': [1.5, 1, 1],
        'Bus': [1.5, 1, 1],
        'Lz/Sz': [2, np.nan, np.nan]
    })
         
    # Erstelle 15-Min-Zeitintervall von 00:00 bis 24:00
    start_time = pd.Timestamp("00:00")
    interval_15 = []
    for i in range(intervall):
        von = start_time + pd.Timedelta(minutes=15 * i)
        bis = von + pd.Timedelta(minutes=15)
        interval_15.append((von.strftime("%H:%M"), bis.strftime("%H:%M")))
    
    # DataFrame für die 15-Min-Intervalle
    df_15min = pd.DataFrame({
        'von': [i[0] for i in interval_15],
        'bis': [i[1] for i in interval_15],
        'PKW-E': [np.nan] * intervall,
        'Kfz': [np.nan] * intervall,
        'SV': [np.nan] * intervall,
        'SV(%)': [np.nan] * intervall
    })
    df15_strom = stromliste(intervall, df_15min)
    # df_15min = pd.concat([df_15min,df15_strom], axis=1)

    df = pd.read_excel(file, sheet_name='DB-01', header=0)
    arme = df.drop_duplicates(['VON_ARM','NACH_ARM'])[['VON_ARM','NACH_ARM']]
    grouped = df.groupby(['VON_ARM', 'NACH_ARM'])
    richtungs_matrices = {}
    for _, row in arme.iterrows():
        von = row['VON_ARM']
        nach = row['NACH_ARM']
        # Zugriff auf eine Gruppe (z.B. A nach C)
        matrix = grouped[['VON_UHR', 'Fg', 'Rad', 'K-Rad', 'Pkw', 'Lfw', 'Lkw', 'Bus', 'Lz/ Sz']].get_group((von, nach))
        matrix[''] = matrix[[]].sum()
        richtungs_matrices[f"{von}_{nach}"] = matrix
    






    file = file.replace('.xlsx','_test.xlsx', 1)
    df_15min.to_excel(file)
    # for id, row in tqdm(df.iterrows()):
    #     matching_rows = df_15min[(df_15min['von'] == row['VON_UHR']) & 
    #                        (df_15min['VON_ARM'] == row['VON_ARM']) & 
    #                        (df_15min['NACH_ARM'] == row['NACH_ARM'])]
    #     if not matching_rows.empty:
    #         idx = matching_rows.index[0] 

    """
    # Erstelle 60-Min-Zeitntervall von 00:00 bis 24:00
    interval_60 = []
    for i in range(24):
        von = start_time + pd.Timedelta(hours= i)
        if intervall <= 24 & i == 23: # Für den 24:00 -> 00:00 Wechsel
            bis = pd.Timestamp("00:00") + pd.Timedelta(days=1)
        else:
            bis = von + pd.Timedelta(hours=1)
        interval_60.append((von.strftime("%H:%M"), bis.strftime("%H:%M")))

    

    # DataFrame für die 60-Min-Intervalle
    df_hourly = pd.DataFrame({
        'von': [i[0] for i in interval_60],
        'bis': [i[1] for i in interval_60],
        'PKW-E': [np.nan] * 24,
        'Kfz': [np.nan] * 24,
        'SV': [np.nan] * 24,
        'SV(%)': [np.nan] * 24
    })


    # Ausgabe der DataFrames (zum Überprüfen)
    print("15-Minuten-Intervalle DataFrame:")
    print(df_15min.head(10))  # Zeige die ersten 10 Zeilen
    print("\nStündliche Intervalle DataFrame:")
    print(df_hourly.head(10))
    print("\nFahrzeugtypen-Faktoren DataFrame:")
    print(vehicle_factors)
    df = pd.read_excel("F:\Rohdaten Kiel 2025.xlsx",sheet_name="01")
    print(df)
    """

if __name__ == "__main__":
    # 
    # convert(r"F:\knoten1_morgen_2025-10-21_15-12-13.counts_15min_reduziert.csv")
    firstpage(r"F:\knoten1_morgen_2025-10-21_15-12-13.counts_15min_reduziert_bueffeeTale.xlsx")