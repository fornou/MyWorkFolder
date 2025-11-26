from sqlalchemy.orm import Session
from model.utente import Utente
from services.token_service import TokenService
from services.auth_service import AuthService, get_current_user
from database.database import get_db
from schemas.auth import CreateUserRequest
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.concurrency import run_in_threadpool

import logging
from services.utente_service import UtenteService
logger = logging.getLogger("auth_controller") 

logging.basicConfig(level=logging.INFO)


class AuthController:
    def __init__(self):
        self.router = APIRouter(prefix="/api/auth", tags=["Auth"])
        self._add_routes()

    def _add_routes(self):
        self.router.post("/signup", status_code=status.HTTP_201_CREATED)(self.create_user)
        self.router.post("/signin")(self.login_user)
        self.router.post("/logout")(self.logout_user)

    # ------------------ SIGNUP ------------------
    async def create_user(self, create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
        try:
            auth_service = AuthService(db)
            token_service = TokenService(db)
            # Esecuzione in thread separato per non bloccare l'event loop
            user = await run_in_threadpool(auth_service.create_user, create_user_request.Email, create_user_request.Password)
            if not user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Creazione utente fallita")

            token = await run_in_threadpool(token_service.create, user)
            if not token:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Creazione token fallita")

            return {"access_token": token.token, "token_type": "bearer"}

        except Exception as e:
            logger.exception("Errore create_user")
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------ SIGNIN ------------------
    async def login_user(self, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        try:
            auth_service = AuthService(db)
            token_service = TokenService(db)
            utente_service = UtenteService(db)

            # Autenticazione e ricerca utente in thread separato
            user = await run_in_threadpool(auth_service.authenticate_user, form_data.username, form_data.password)
            username = await run_in_threadpool(utente_service.get_utente_by_email, form_data.username)

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

            # Aggiornamento token in thread separato
            await run_in_threadpool(token_service.update_token, user.ID_Utente, True, True)
            token = await run_in_threadpool(token_service.create, user)
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

        except Exception as e:
            logger.exception("Errore login_user")
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------ LOGOUT ------------------
    async def logout_user(self, db: Session = Depends(get_db), current_user: Utente = Depends(get_current_user)):
        try:
            id_utente = int(current_user.ID_Utente)
            token_service = TokenService(db)
            await run_in_threadpool(token_service.update_token, id_utente, True, True)
            return {"message": "Logout effettuato"}

        except Exception as e:
            logger.exception("Errore logout_user")
            raise HTTPException(status_code=500, detail="Logout fallito")