from sqlalchemy.orm import Session, joinedload
from model.token import Token
from sqlalchemy import func
from datetime import datetime

class TokenDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Token).all()

    def create(self, user_id: int, access_token: str, expiration_time: datetime):
        new_token = Token(
            user_id=user_id,
            token=access_token,
            revocato=False,
            espirato=False,
            created_at=datetime.now(),
            expires_at=expiration_time
        )
        self.db.add(new_token)
        self.db.commit()
        self.db.refresh(new_token)
        return new_token

    def get_by_token(self, token: str):
        return self.db.query(Token).options(joinedload(Token.utente)).filter(Token.token == token).first()
    
    def get_all_by_user_id(self, user_id: int):
        return self.db.query(Token).filter(Token.user_id == user_id).all()
    
    def update_espirato(self, token: str, espirato: bool):
        self.db.query(Token).filter(Token.token == token).update({Token.espirato: espirato}, synchronize_session=False)
        self.db.commit()

    #Aggiorna i token di uno specifico utente e non scaduti o revocati
    def update_token(self, user_id: int, espirato: bool, revocato: bool):
        self.db.query(Token).filter(
            Token.user_id == user_id,
            Token.espirato == False,
            Token.revocato == False
        ).update({Token.revocato: revocato, Token.espirato: espirato}, synchronize_session=False)
        self.db.commit()