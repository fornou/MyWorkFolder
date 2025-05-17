from pathlib import Path
import pandas as pd

class FormattatoreCsv:
    def __init__(self, url, colonne_date: list, commessa):
        self.commessa = commessa
        self.url = self.esiste_file(url)
        self.df = self.traduci_colonne()
        self.colonne_date = colonne_date

    def traduci_colonne(self):
        df = pd.read_csv(self.url, sep=';', encoding='utf-8', dtype=str)

        if self.commessa == "3":
            print("Commessa 3 - Traduzione colonne attivata.")

            col_mapping = {
                'Date\\time TX': 'Data\\Ora TX',
                'Machine': 'Macchina',
                'Type': 'Tipo',
                'Result': 'Risultati',
                'Date\\time RX': 'Data\\Ora RX',
                'Quote': 'Quota',
                '# PLC': '# PLC',
                '# LU': '# UDC',
                'Row': 'Cella',
                'Destination': 'Destinazione',
                'Start': 'Inizio',
                'End': 'Fine',
                'Start quote': 'Quota inizio',
                'Start date\\time': 'Data\\Ora inizio',
                'Distance': 'Distanza',
                'Timespan': 'Durata',
                'Direction': 'Direzione',
                'Logical state': 'Stato logico',
                'Index': 'Indice',
                'Num. missions': 'Num. missioni',
                'Note': 'Note',
                'Battery Level Tx': 'Livello Batteria Tx',
                'Battery Level Rx': 'Livello Batteria Rx',
                'Encoder Value Tx': 'Valore encoder Tx',
                'LU Weight': 'Peso UDC',
                'Parameters': 'Parametri'
            }
            df = df.rename(columns=col_mapping)

            # Traduzione dei valori nella colonna "Tipo"
            tipo_mapping = {
                "(10) Taking": "(10) Prelievo",
                "(10) Taking with chain": "(10) Prelievo con catena",
                "(12) Taking without lifter": "(12) Prelievo senza lifter",
                "(20) Leaving": "(20) Deposito",
                "(20) Leaving with chain": "(20) Deposito con catena",
                "(30) Move": "(30) Spostamento",
                "(31) Move partial": "(31) Movimento parziale",
                "(40) Move in": "(40) Ingresso",
                "(41) Move in from partial quote": "(41) Ingresso da quota parziale",
                "(50) Move out": "(50) Uscita",
                "(51) Move out partial": "(51) Uscita parziale",
                "(60) Positioning with chains": "(60) Posizionamento con catene",
                "(91) Disable battery": "(91) Disabilita batteria",
                "(92) Enable battery": "(92) Abilita batteria"
            }
            if "Tipo" in df.columns:
                df["Tipo"] = df["Tipo"].map(tipo_mapping).fillna(df["Tipo"])  # Mantiene i valori non mappati

            # Traduzione dei valori nella colonna "Risultati"
            risultato_mapping = {
                "(111) Invalid logical state": "(111) Stato logico non valido",
                "(122) Error warning": "(122) Errore warning",
                "(24) OK but quote Tx": "(24) OK quota teorica",
                "(215) Automatic manual": "(215) Automatico manuale",
                "(200) Alarm Hardware": "(200) AlarmHW"
            }
            if "Risultati" in df.columns:
                df["Risultati"] = df["Risultati"].map(risultato_mapping).fillna(df["Risultati"]) 
        else:
            print(f"Commessa {self.commessa} - Nessuna traduzione colonne.")

        return df

    def esiste_file(self, url):
        file_path = Path(url)
        if not file_path.is_file():
            raise FileNotFoundError(f"Errore: Il file {url} non esiste.")
        return file_path

    def converti_date(self, colonne: list = None):
        if not colonne:
            colonne = self.colonne_date
        for colonna in colonne:
            self.df[colonna] = pd.to_datetime(self.df[colonna], errors='coerce')

    def aggiungi_campo(self):
        self.df.insert(0, 'ID_Commissione', self.commessa)

    def get_url_destinazione(self):
        return str(self.url.parent / f"{self.url.stem}_elaborato.csv")

    def esporta_file(self):
        try:
            self.df.to_csv(self.get_url_destinazione(), sep=';', index=False, encoding='utf-8')
            print(f'Il percorso del file aggiornato: {self.get_url_destinazione()}')
        except PermissionError:
            print(f"Errore: Il file {self.get_url_destinazione()} è aperto in un altro programma. Chiudi il file e riprova.")
        except Exception as e:
            print(f"Si è verificato un errore durante il salvataggio del file: {e}")
