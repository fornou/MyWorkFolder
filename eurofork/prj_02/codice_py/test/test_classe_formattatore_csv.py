import pandas as pd

def mappa_e_prepara_records(df, mapping, commessa_id, col_data_commessa="ID_Commessa"):
    records = []
    for _, row in df.iterrows():
        record = {}
        for csv_col, db_col in mapping.items():
            record[db_col] = row.get(csv_col)
        record[col_data_commessa] = commessa_id
        records.append(record)
    return records

def carica_e_filtra_csv_micromissioni(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        
        df.columns = df.columns.str.strip()

        colonne_date = ['Date\\time TX', 'Date\\time RX', 'Start date\\time']
        for col in colonne_date:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        return df
    except Exception as e:
        raise ValueError(f"Errore nel caricamento micromissioni: {e}")

def carica_e_filtra_csv_allarmi(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()

        colonne_date = ['Date time']
        for col in colonne_date:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        return df
    except Exception as e:
        raise ValueError(f"Errore nel caricamento allarmi: {e}")
