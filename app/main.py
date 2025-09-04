from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import pais

# Crear tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Paises")

# 🔹 Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes poner ["http://localhost:4200", "https://tu-front.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(pais.router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
