from sqlalchemy.orm import Session
from model.utente import Utente
from services.token_service import TokenService
from services.auth_service import AuthService
from database.database import get_db
from services.auth_service import get_current_user
from schemas.auth import CreateUserRequest
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import  OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Security



class AuthController:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["Auth"])
        self._add_routes()

    def _add_routes(self):
        self.router.post("/signup", status_code=status.HTTP_201_CREATED)(self.create_user)
        self.router.post("/signin")(self.login_user)
        self.router.post("/logout/{user_id}")(self.logout_user)
        # self.router.get("/area-protetta")(self.protected_route)

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

        user = auth_service.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_service.update_token(user.ID_Utente, False, False)
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

    async def logout_user(self, user_id: int, db: Session = Depends(get_db), current_user: Utente = Depends(get_current_user)):
        if current_user.ID_Utente != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Non autorizzato")
        token_service = TokenService(db)
        token_service.update_token(user_id, True, True)
        return {"message": "Logout effettuato"}


    # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin") # recupera il token dall'header (Authorization: Bearer <token>)

    # async def protected_route(self, token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    #     token_service = TokenService(db)
    #     utente = token_service.token_validation(token)
    #     if not utente:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token non valido o scaduto")
    #     return {"message": "Accesso autorizzato"}
