from sqlalchemy.orm import Session
from model.utente import Utente
from services.token_service import TokenService
from services.auth_service import AuthService
from database.database import get_db
from services.auth_service import get_current_user
from schemas.auth import CreateUserRequest
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import  OAuth2PasswordRequestForm
import logging

from services.utente_service import UtenteService
logger = logging.getLogger(__name__)


class AuthController:
    def __init__(self):
        self.router = APIRouter(prefix="/api/auth", tags=["Auth"])
        self._add_routes()

    def _add_routes(self):
        self.router.post("/signup", status_code=status.HTTP_201_CREATED)(self.create_user)
        self.router.post("/signin")(self.login_user)
        self.router.post("/logout")(self.logout_user)

    async def create_user(self, create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
        auth_service = AuthService(db)
        token_service = TokenService(db)

        user = auth_service.create_user(create_user_request.Email, create_user_request.Password)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Creazione utente fallita")

        token = token_service.create(user)
        if not token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Creazione token fallita")

        return {"access_token": token.token, "token_type": "bearer"}

    async def login_user(self, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        auth_service = AuthService(db)
        token_service = TokenService(db)
        utente_service = UtenteService(db)

        user = auth_service.authenticate_user(form_data.username, form_data.password)
        username = utente_service.get_utente_by_email(form_data.username)
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email non registrata",
                headers={"WWW-Authenticate": "Bearer"}
            )
        elif not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password errata",
                headers={"WWW-Authenticate": "Bearer"}
            )


        token_service.update_token(user.ID_Utente, True, True)
        token = token_service.create(user)
        if not token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Creazione token fallita")

        return {
            "access_token": token.token,
            "token_type": "bearer",
            "user": {
                "id": user.ID_Utente,
                "email": user.Email
            }
        }

    async def logout_user(self,db: Session = Depends(get_db), current_user: Utente = Depends(get_current_user)):
        id_utente = int(current_user.ID_Utente)
        try:
            token_service = TokenService(db)
            token_service.update_token(id_utente, True, True)
            return {"message": "Logout effettuato"}
        except:
            return {"message": "Logout fallito"}