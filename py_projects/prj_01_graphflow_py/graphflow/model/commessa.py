from sqlalchemy import Column, Integer, String
from database.database import Base 
from sqlalchemy.orm import relationship

class Commessa(Base):
    __tablename__ = 'Commesse'
    
    ID_Commessa = Column(Integer, primary_key=True, index = True, autoincrement=True) 
    Nome = Column(String(255), nullable=False)  
    
    micro_missioni = relationship("MicroMissioni", back_populates="commessa", cascade="all, delete-orphan")
    allarmi = relationship("Allarmi", back_populates="commessa", cascade="all, delete-orphan")

