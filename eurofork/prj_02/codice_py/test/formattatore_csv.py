from pathlib import Path
import pandas as pd

class formattatore_csv:

    def __init__(self, url, colonne_date: list, commessa):
        self.commessa = commessa
        self.url = self.esiste_file(url)
        self.df = self.traduci_colonne(url)
        self.colonne_date = colonne_date

    def __init__(self, url, colonna_data):	
        self.url = self.esiste_file(url)
        self.df = pd.read_csv(url, sep=';', encoding='utf-8', dtype=str)
        self.colonna_date = colonna_data
        											                                                                                    			
    def traduci_colonne(self, url):
        df = pd.read_csv(url, sep=';', encoding='utf-8', dtype=str)
        if self.commessa == 3:
            df.columns = [
                            'Data\\Ora TX', 'Macchina', 'Tipo', 'Risultati', 'Data\\Ora RX',
                            'Quota', '# PLC', '# UDC', 'Cella', 'Destinazione', 'Inizio', 
                            'Fine', 'Quota inizio', 'Data\\Ora inizio', 'Distanza', 'Durata', 
                            'Direzione', 'Stato logico', 'Indice', 'Num. missioni', 'Note',
                            'Livello Batteria Tx', 'Livello Batteria Rx', 'Valore encoder Tx',
                            'Peso UDC', 'Parameters'
                        ]
        return df
    

    def esiste_file(self, url):
        file_path = Path(url)
        if not file_path.is_file():
            print(f"Errore: Il file {url} non esiste.")
        return file_path

    def converti_date(self, colonne: list = None):
        if not colonne:
            colonne = self.colonne_date
        for colonna in colonne:
            self.df[colonna] = pd.to_datetime(self.df[colonna], errors='coerce')

    def testa_conversione(self):
        colonna = 'Data\\Ora TX'
        print(self.df[colonna].dtype)
        print(self.df[colonna].head(10))
        self.converti_date([colonna]) 
        print(self.df[colonna].dtype)
        print(self.df[colonna].head(10))

    def aggiungi_campo(self):
        self.df.insert(0, 'ID_Commissione', self.commessa)

    def get_url_destinazione(self):
        destinazione = self.url.parents[1] / f"file_formattati/{self.url.stem}_elaborato.csv"
        destinazione.parent.mkdir(parents=True, exist_ok=True)  # crea le directory non esistenti
        return destinazione

    def get_nome_file(self):
        return self.url.stem

    def esporta_file(self):
        try:
            self.df.to_csv(self.get_url_destinazione(), sep=';', index=False, encoding='utf-8')
            print(f'Il percorso del file aggiornato: {self.get_url_destinazione()}')
        except PermissionError:
            print(f"Errore: Il file {self.get_url_destinazione()} è aperto in un altro programma. Chiudi il file e riprova.")
        except Exception as e:
            print(f"Si è verificato un errore durante il salvataggio del file: {e}")
