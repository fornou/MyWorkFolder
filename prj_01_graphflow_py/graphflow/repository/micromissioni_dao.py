from sqlalchemy.orm import Session
from model.micromissioni import MicroMissioni
import time

class MicroMissioniDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(MicroMissioni).all()

    def get_by_id(self, id_micromissione: int):
        return (
            self.db.query(MicroMissioni)
            .filter(MicroMissioni.ID_Micromissione == id_micromissione)
            .first()
        )

    def get_by_commessa_id(self, id_commessa: int):
        return (
            self.db.query(MicroMissioni)
            .filter(MicroMissioni.ID_Commessa == id_commessa)
            .all()
        )

    def create(self, data: dict):
        nuova = MicroMissioni(**data)
        self.db.add(nuova)
        self.db.commit()
        self.db.refresh(nuova)
        return nuova
    
    def bulk_create(self, data_list: list[dict], batch_size: int = 1000):
        start = time.time()

        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i+batch_size]
            self.db.bulk_insert_mappings(MicroMissioni, batch)
            self.db.commit()
            print(f"✅ Inseriti {i + len(batch)} record su {len(data_list)}...")
            
        print(f"⏱️ Inserimento completato in {time.time() - start:.2f} secondi")