from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Billete(Base):
    __tablename__ = "billetes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    anverso = Column(String, nullable=False)
    reverso = Column(String, nullable=False)
    pais = Column(Integer, ForeignKey("paises.id"), nullable=False)

    pais_rel = relationship("Pais", backref="billetes")