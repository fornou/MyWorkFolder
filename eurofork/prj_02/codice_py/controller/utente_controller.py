from fastapi import  Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from model.utente import StatoAdmin, Utente
from services.auth_service import get_current_user
from services.token_service import TokenService
from services.utente_service import UtenteService

class UtenteController:
    def __init__(self):
        self.router = APIRouter(prefix="/api/utente", tags=["Utenti"])#, dependencies=[Depends(get_current_user)])
        self._add_routes()

    def _add_routes(self):
        self.router.get("/all")(self.get_all_utenti)
        self.router.get("/me")(self.get_my_data)
        self.router.get("/{id}/tokens")(self.get_all_tokens_by_id)
        self.router.get("/{id}")(self.get_utente_by_id)

    def get_all_utenti(self, db: Session = Depends(get_db)):
        return UtenteService(db).list_utenti()
    
    def get_all_tokens_by_id(self, id: int, current_user: Utente = Depends(get_current_user), db: Session = Depends(get_db)):
        # Controllo: solo l'utente proprietario o un admin può accedere
        if current_user.ID_Utente != id and current_user.Is_Admin == StatoAdmin.no:
            raise HTTPException(status_code=403, detail="Non autorizzato")
        return TokenService(db).list_tokens_by_utente(id)
    
    def get_utente_by_id(self, id: int, db: Session = Depends(get_db)):
        return UtenteService(db).get_utente_by_id(id)
    
    def get_my_data(self, current_user: Utente = Depends(get_current_user)):
        return current_user