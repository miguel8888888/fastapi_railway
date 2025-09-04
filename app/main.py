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
    allow_origins=["*"],  # ajusta a tus dominios si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Middleware para evitar cache en Railway / navegadores
@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Routers
app.include_router(pais.router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

