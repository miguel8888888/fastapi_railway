from fastapi import FastAPI
from app.database import engine, Base
from app.routers import pais

# Crear tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Paises")

app.include_router(pais.router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
