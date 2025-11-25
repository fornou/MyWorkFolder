import pandas as pd

def mappa_e_prepara_records(df, mapping, commessa_id, col_data_commessa="ID_Commessa"):
    records = []
    for i, (_, row) in enumerate(df.iterrows()):
        record = {}
        for csv_col, db_col in mapping.items():
            val = row.get(csv_col)
            if pd.isna(val):  # intercetta NaN, NaT, None
                val = None
            record[db_col] = val
        record[col_data_commessa] = commessa_id
        records.append(record)

        if i % 1000 == 0:
            print(f"🧱 Mappati {i} record...")

    print(f"✅ Totale record mappati: {len(records)}")
    print("Esempio record: ", records[0])
    return records


def converti_date(df, date_cols):
    for col in date_cols:
        if col in df.columns:
            original_nonempty = df[col].notna().sum()
            df[col] = pd.to_datetime(df[col], format="%m/%d/%Y %I:%M:%S %p", errors='coerce')
            df[col] = df[col].where(df[col].notna(), None)
            parsed_count = df[col].notna().sum()
            print(f"📆 Colonna '{col}': convertiti {parsed_count}/{original_nonempty} valori.")
    return df


def carica_e_filtra_csv_micromissioni(filepath):
    df = pd.read_csv(filepath, sep=';')
    return converti_date(df, ['Date\\time TX', 'Date\\time RX', 'Start date\\time'])

def carica_e_filtra_csv_allarmi(filepath):
    df = pd.read_csv(filepath, sep=';')
    return converti_date(df, ['Date time'])
