from repository.commessa_dao import CommessaDAO
from sqlalchemy.orm import Session

class CommessaService:
    def __init__(self, db: Session):
        self.dao = CommessaDAO(db)

    def list_commesse(self):
        return self.dao.get_all()

    def get_commessa_by_id(self, commessa_id: int):
        return self.dao.get_by_id(commessa_id)

    def get_commessa_by_nome(self, nome: str):
        return self.dao.get_by_nome(nome)

    def search_commesse(self, title: str):
        return self.dao.get_by_filter(title)

    def add_commessa(self, nome: str):
        return self.dao.create(nome)
