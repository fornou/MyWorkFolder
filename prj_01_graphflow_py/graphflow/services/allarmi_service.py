from sqlalchemy.orm import Session
from repository.allarmi_dao import AllarmiDAO
from util.csv_utils import mappa_e_prepara_records

MAPPING_COLONNE_ALLARMI = {
    "Date_time": "Data_Ora",
    "Type": "Tipo",
    "Peripheral_name": "Macchina",
    "Value": "Valore",
    "Code": "Codice",
    "Description": "Descrizione",
    "Encoder": "Encoder"
}

class AllarmiService:
    def __init__(self, db: Session):
        self.dao = AllarmiDAO(db)

    def list_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_allarme: int):
        return self.dao.get_by_id(id_allarme)

    def get_by_commessa(self, commessa_id: int):
        return self.dao.get_by_commessa_id(commessa_id)

    def carica_allarmi(self, commessa_id: int, df):
        print("Inizio replace \\ ")
        df.columns = [
            col.replace("\\", "_").replace(" ", "_").strip()
            for col in df.columns
        ]
        print("Fine replace \\ e Inizio assegnazione tipo")

        def assegna_tipo(codice):
            if "DB126" in codice:
                return "Silent Warning"
            elif "DB116" in codice:
                return "Warning"
            elif "DB106" in codice:
                return "Alarm"
            else:
                return "Sconosciuto"

        df["Type"] = df["Code"].fillna("").apply(assegna_tipo)

        print("Fine assegnazione tipo e Inizio mappatura")

        records = mappa_e_prepara_records(
            df,
            MAPPING_COLONNE_ALLARMI, 
            commessa_id, 
            col_data_commessa="ID_Commessa"
        )

        print("Fine mappatura e Inizio bulk_create")        
        self.dao.bulk_create(records)