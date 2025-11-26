from sqlalchemy import Column, Integer, String, DateTime, Float
from database.database import Base  # importa la tua Base di SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Allarmi(Base):
    __tablename__ = "Allarmi"

    ID = Column(Integer, primary_key=True, index=True)
    Data_Ora = Column(DateTime, nullable=True)
    Tipo = Column(String(150), nullable=True)
    Macchina = Column(String(150), nullable=True)
    Valore = Column(String(10), nullable=True)
    Codice = Column(String(150), nullable=True)
    Descrizione = Column(String(150), nullable=True)

    ID_Commessa = Column(Integer, ForeignKey("Commesse.ID_Commessa"), nullable=False)
    commessa = relationship("Commessa", back_populates="allarmi") 
