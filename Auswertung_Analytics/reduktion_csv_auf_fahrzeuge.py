# UTF-8
import pandas as pd

def reduktion_df(file_path, sep=',') -> None:
    typ = ('bicycle', 'bus', 'car', 'motorcycle', 'person', 'train', 'truck')
    df = pd.read_csv(file_path, sep=sep, header=0, encoding='utf-8')
    df_reduziert = df[df['classification'].isin(typ)]
    df = df[~df['classification'].isin(typ)]
    print(f"Es wurden {len(df_reduziert)} gefunden. {len(df)} Kategorien wurden aufgrund einer nicht passende Kategorie reduziert. Darin sind {df['count'].sum()} Werte, die das System erkannt hat.")
    df_reduziert.to_csv(file_path.replace('.csv','_reduziert.csv', 1), index=False)

def zusammenfassen() -> object:
    s1 = r"D:\Erhebungen\06-2025 Böhler\12-06_06-00\2025-06-25_15-21-20.counts_15min.csv"
    df1 = pd.read_csv(s1, sep=',', header=0, encoding='utf-8')
    s2 = r"D:\Erhebungen\06-2025 Böhler\12-06_14-00\2025-06-25_15-26-49.counts_15min.csv"
    df2 = pd.read_csv(s2, sep=',', header=0, encoding='utf-8')
    df3 = pd.concat([df1, df2], axis=0, ignore_index=True)
    df3.to_csv(r"D:\Erhebungen\06-2025 Böhler\Böhler12_06_2025.csv", index=False)

if __name__ == "__main__":
    #zusammenfassen()
    reduktion_df(r"D:\Erhebungen\07-2025 Rheinbahn Düsseldorf\Video\01.07.2025\cam2\16-18Uhr\2025-07-14_12-26-35.counts_15min.csv")
    # path = input('Dateipfad bitte Angeben: ')
    # try:
    #     reduktion_df(path)
    # except Exception as e:
    #     print(f'Fehler: {e}')
    
