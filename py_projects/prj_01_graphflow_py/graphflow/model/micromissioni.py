from sqlalchemy import Column, Integer, String, DateTime, Time
from database.database import Base  # importa la tua Base di SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class MicroMissioni(Base):
    __tablename__ = "MicroMissioni"

    ID_Micromissione = Column(Integer, primary_key=True, autoincrement=True)
    Data_Ora_Tx = Column(DateTime, nullable=True)
    Macchina = Column(String(100), nullable=True)
    Tipo = Column(String(50), nullable=True)
    Risultato = Column(String(50), nullable=True)
    Data_Ora_Rx = Column(DateTime, nullable=True)
    Quota_Finale_Teorica = Column(Integer, nullable=True)
    PLC = Column(String(50), nullable=True)
    UDC = Column(String(50), nullable=True)
    Cella = Column(String(50), nullable=True)
    Quota_Finale_Effettiva = Column(Integer, nullable=True)
    Inizio = Column(Integer, nullable=True)
    Fine = Column(Integer, nullable=True)
    Quota_Inizio = Column(Integer, nullable=True)
    Data_Ora_Inizio = Column(DateTime, nullable=True)
    Distanza = Column(Integer, nullable=True)
    Durata = Column(Time, nullable=True)
    Direzione = Column(String(20), nullable=True)
    Stato_logico = Column(String(20), nullable=True)
    Indice_Micromissione = Column(Integer, nullable=True)
    Numero_Micromissioni = Column(Integer, nullable=True)
    Note = Column(String(100), nullable=True)
    Livello_Batteria_Tx = Column(Integer, nullable=True, default=0)
    Livello_Batteria_Rx = Column(Integer, nullable=True, default=0)
    Valore_encoder_Tx = Column(Integer, nullable=True, default=0)
    Peso_UDC = Column(Integer, nullable=True)

    ID_Commessa = Column(Integer, ForeignKey("Commesse.ID_Commessa"), nullable=False)
    commessa = relationship("Commessa", back_populates="micro_missioni") 
