from fastapi import FastAPI
from controller.commessa_controller import CommessaController
from controller.utente_controller import UtenteController
from controller.mvc import MVCController
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from database.database import init_db
from database.settings import settings
from controller.auth_controller import AuthController


def create_app():
    app = FastAPI()

    commessa_controller = CommessaController()
    utente_controller = UtenteController()
    mvc_controller = MVCController()
    auth_controller = AuthController()

    app.include_router(commessa_controller.router)
    app.include_router(utente_controller.router)
    app.include_router(auth_controller.router)
    app.include_router(mvc_controller.router)

    app.mount("/static", StaticFiles(directory="resources/static"), name="static")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],  # consente tutti i metodi
        allow_headers=["*"],  # consente tutti gli header
    )

    if settings.INIT_DB_AT_STARTUP:
        init_db()
        print("Database inizializzato")

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="La tua API",
            version="1.0.0",
            description="API con autenticazione JWT",
            routes=app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
        for path in openapi_schema["paths"].values():
            for operation in path.values():
                operation["security"] = [{"BearerAuth": []}]
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi

    return app

app = create_app()
