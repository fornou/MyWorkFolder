from sqlalchemy import Column, Integer, String
from database.database import Base 

class Commessa(Base):
    __tablename__ = 'Commesse'
    
    ID_Commessa = Column(Integer, primary_key=True, index = True, autoincrement=True) 
    Nome = Column(String(255), nullable=False)  
