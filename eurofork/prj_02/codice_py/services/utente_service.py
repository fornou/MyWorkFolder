from repository.utente_dao import UtenteDAO
from sqlalchemy.orm import Session

class UtenteService:
    def __init__(self, db: Session):
        self.dao = UtenteDAO(db)

    def list_utenti(self):
        return self.dao.get_all()
    
    def create(self, email: str, password: str):
        return self.dao.create(email, password)
    
    def get_utente_by_id(self, id: int):
        return self.dao.get_by_id(id)