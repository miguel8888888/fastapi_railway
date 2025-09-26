from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Render expone la cadena completa en DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://db_numismatica_user:F0TkUKIbTcCBMyIofXnHyRHNNfEVU3Uy@dpg-d39jv3c9c44c73fjhrsg-a.oregon-postgres.render.com/db_numismatica"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener sesión DB en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()