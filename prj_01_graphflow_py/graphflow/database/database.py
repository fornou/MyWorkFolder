from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .settings import settings
import importlib
import pkgutil
from model import __path__ as model_path

# crea una connessione al database
engine = create_engine(settings.db_url, pool_pre_ping=True)

# Crea il sessionmaker per gestire le sessioni e la collega all'engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base per i modelli/oggetti
Base = declarative_base()

class Database:
    def __init__(self):
        self.db_session: Session = None

    def open_connection(self) -> Session:
        """Apre una nuova connessione al database e ritorna la sessione"""
        if self.db_session is None:
            self.db_session = SessionLocal()  # Apre una nuova sessione
        return self.db_session

    def close_connection(self):
        """Chiude la connessione al database"""
        if self.db_session:
            self.db_session.close()  # Chiude la sessione
            self.db_session = None

    def commit(self):
        """Commit della transazione"""
        if self.db_session:
            self.db_session.commit()

    def rollback(self):
        """Rollback della transazione in caso d'errore"""
        if self.db_session:
            self.db_session.rollback()

    def get_session(self) -> Session:
        """Restituisce la sessione corrente"""
        return self.db_session


db_instance = Database()

def get_db():
    db = db_instance.open_connection()  # apre la sessione (se non già aperta)
    try:
        yield db                       # "passa" la sessione a chi la chiama (FastAPI)
    finally:
        db_instance.close_connection()  # chiude la sessione dopo la risposta

def init_db():
    # Importa dinamicamente tutti i moduli che definiscono modelli
    for _, module_name, _ in pkgutil.iter_modules(model_path):
        if not module_name.startswith("_"):  # evita __init__.py o moduli privati
            importlib.import_module(f"model.{module_name}")

    # Crea tutte le tabelle
    Base.metadata.create_all(bind=engine)
    print("Tabelle create:", list(Base.metadata.tables.keys()))

