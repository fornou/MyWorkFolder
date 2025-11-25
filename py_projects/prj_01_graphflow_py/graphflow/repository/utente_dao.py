from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from model.utente import Utente

class UtenteDAO:
    def __init__(self, db : Session):
        self.db = db

    def get_all(self):
        return self.db.query(Utente).all()
    
    def get_by_email(self, email: str) -> Optional[Utente]:
        return self.db.query(Utente).filter(Utente.Email == email).first()
    
    def get_by_id(self, user_id: int) -> Optional[Utente]:
        return self.db.query(Utente).filter(Utente.ID_Utente == user_id).first()
    
    def create(self, email: str, password: str):
        new_user = Utente(Email=email, Password=password)
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email già registrata"
            )
        
    def delete(self, user_id: int):
        user = self.db.query(Utente).get(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()

    def update_password(self, user_id: int, new_password: str):
        user = self.db.query(Utente).get(user_id)
        if user:
            user.Password = new_password
            self.db.commit()