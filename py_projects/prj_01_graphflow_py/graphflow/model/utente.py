from sqlalchemy import Enum, Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base
import enum

class StatoAdmin(str, enum.Enum):
    si = "S"
    no = "N"

class Utente(Base):
    __tablename__ = "Utenti"

    ID_Utente = Column(Integer, primary_key=True, index=True)
    Email = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Is_Admin = Column(Enum(StatoAdmin), nullable=False, default=StatoAdmin.no)

    tokens = relationship("Token", back_populates="utente")
