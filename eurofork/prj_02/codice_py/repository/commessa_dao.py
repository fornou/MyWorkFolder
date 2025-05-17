from sqlalchemy.orm import Session
from model.commessa import Commessa
from sqlalchemy import func

class CommessaDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Commessa).all()
    
    def get_by_nome(self, commessa: str):
        return self.db.query(Commessa).filter(Commessa.Nome == commessa).first()

    def get_by_id(self, commessa_id: int):
        return self.db.query(Commessa).filter(Commessa.ID_Commessa == commessa_id).first()

    def get_by_filter(self, title: str):
        return self.db.query(Commessa).filter(func.lower(Commessa.Nome).contains(title.lower())).all()

    def create(self, nome: str):
        nuova = Commessa(Nome=nome)
        self.db.add(nuova)
        self.db.commit()
        self.db.refresh(nuova)
        return nuova
