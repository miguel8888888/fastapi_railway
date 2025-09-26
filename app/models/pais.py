from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Pais(Base):
    __tablename__ = "paises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pais = Column(String, nullable=False)
    bandera = Column(Text, nullable=True)
    continente = Column(String, nullable=True)
