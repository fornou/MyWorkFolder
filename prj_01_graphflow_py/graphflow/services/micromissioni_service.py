from sqlalchemy.orm import Session
from repository.micromissioni_dao import MicroMissioniDAO
from util.csv_utils import mappa_e_prepara_records

MAPPING_COLONNE_MICROMISSIONI = {
    "Date_time_TX": "Data_Ora_Tx",
    "Machine": "Macchina",
    "Type": "Tipo",
    "Result": "Risultato",
    "Date_time_RX": "Data_Ora_Rx",
    "Quote": "Quota_Finale_Teorica",
    "PLC": "PLC",
    "LU": "UDC",
    "Row": "Cella",
    "Destination": "Quota_Finale_Effettiva",
    "Start": "Inizio",
    "End": "Fine",
    "Start_quote": "Quota_Inizio",
    "Start_date_time": "Data_Ora_Inizio",
    "Distance": "Distanza",
    "Timespan": "Durata",
    "Direction": "Direzione",
    "Logical_state": "Stato_logico",
    "Index": "Indice_Micromissione",
    "Num._missions": "Numero_Micromissioni",
    "Note": "Note",
    "Battery_Level_Tx": "Livello_Batteria_Tx",
    "Battery_Level_Rx": "Livello_Batteria_Rx",
    "Encoder_Value_Tx": "Valore_encoder_Tx",
    "LU_Weight": "Peso_UDC"
}

class MicroMissioniService:
    def __init__(self, db: Session):
        self.dao = MicroMissioniDAO(db)

    def list_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_micromissione: int):
        return self.dao.get_by_id(id_micromissione)

    def get_by_commessa(self, commessa_id: int):
        return self.dao.get_by_commessa_id(commessa_id)

    def carica_micromissioni(self, commessa_id: int, df):

        print("Inizio replace \\ ")
        df.columns = [
            col.replace("\\", "_").replace(" ", "_").strip()
            for col in df.columns
        ]
        print("Fine replace \\ e Inizio mappatura ")

        records = mappa_e_prepara_records(
            df, 
            MAPPING_COLONNE_MICROMISSIONI,
            commessa_id, 
            col_data_commessa="ID_Commessa"
        )

        print("Fine mappatura e Inizio bulk_create")
        self.dao.bulk_create(records)