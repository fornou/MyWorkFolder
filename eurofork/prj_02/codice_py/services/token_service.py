from datetime import datetime, timedelta
from model.utente import Utente
from services import jwt_service
from fastapi import HTTPException
from repository.token_dao import TokenDAO
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

class TokenService:
    def __init__(self, db: Session):
        self.dao = TokenDAO(db)

    def list_tokens_by_utente(self, user_id: int):
        return self.dao.get_all_by_user_id(user_id)
    
    def create(self, user: Utente):
        time_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)) 

        access_token = jwt_service.create_access_token(
            data={"sub": user.Email, "id": user.ID_Utente},
            expires_delta=time_delta
        )
        
        expiration_time = datetime.now() + time_delta

        return self.dao.create(user.ID_Utente, access_token, expiration_time)
    
    def get_by_token(self, token: str):
        return self.dao.get_by_token(token)
    
    def token_validation(self, token: str):
        token_record = self.get_by_token(token)
        
        if not token_record:
            raise HTTPException(status_code=401, detail="Token inesistente")

        if datetime.now() > token_record.expires_at:
            self.dao.update_espirato(token, True)
            raise HTTPException(status_code=401, detail="Token scaduto")

        if token_record.revocato:
            raise HTTPException(status_code=401, detail="Token revocato")

        return token_record.utente
    
    def update_token(self, user_id: int, espirato: bool, revocato: bool):
        self.dao.update_token(user_id, espirato, revocato)
    