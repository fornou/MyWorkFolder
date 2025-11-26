from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Token(Base):
    __tablename__ = "Tokens"

    ID_Token = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Utenti.ID_Utente"), nullable=False)
    token = Column(String(512), nullable=False)
    revocato = Column(Boolean, default=False)
    espirato = Column(Boolean, default=False)
    created_at = Column(DateTime)
    expires_at = Column(DateTime)

    utente = relationship("Utente", back_populates="tokens")
