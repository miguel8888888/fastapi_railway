from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Variables de entorno
# postgresql://postgres:edCDJOBJPvuRByUSMSkmOdbemJyDGRdh@turntable.proxy.rlwy.net:19716/railway
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "edCDJOBJPvuRByUSMSkmOdbemJyDGRdh")
DB_HOST = os.getenv("DB_HOST", "turntable.proxy.rlwy.net")
DB_PORT = os.getenv("DB_PORT", "19716")
DB_NAME = os.getenv("DB_NAME", "railway")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
