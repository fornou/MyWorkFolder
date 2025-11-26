from sqlalchemy.orm import Session
from model.allarmi import Allarmi
import time

class AllarmiDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Allarmi).all()

    def get_by_id(self, id_allarme: int):
        return (
            self.db.query(Allarmi)
            .filter(Allarmi.ID == id_allarme)
            .first()
        )

    def get_by_commessa_id(self, id_commessa: int):
        return (
            self.db.query(Allarmi)
            .filter(Allarmi.ID_Commessa == id_commessa)
            .all()
        )

    def create(self, data: dict):
        nuovo = Allarmi(**data)
        self.db.add(nuovo)
        self.db.commit()
        self.db.refresh(nuovo)
        return nuovo
    
    def bulk_create(self, data_list: list[dict], batch_size: int = 1000):
        start = time.time()

        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i+batch_size]
            self.db.bulk_insert_mappings(Allarmi, batch)
            self.db.commit()
            print(f"✅ Inseriti {i + len(batch)} record su {len(data_list)}...")
            
        print(f"⏱️ Inserimento completato in {time.time() - start:.2f} secondi")