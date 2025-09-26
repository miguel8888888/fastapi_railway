from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import pais
from app.routers import billetes
import os

# Crear tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Paises y Billetes")

# 🔹 Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajusta a tus dominios si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Middleware para evitar cache
@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 🔹 Configuración de uploads para Render (temporal storage)
UPLOAD_DIR = "./uploads"  # directorio temporal en Render
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Servir archivos estáticos
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Endpoint para subir imágenes
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"url": f"uploads/{file.filename}"}

# Routers
app.include_router(pais.router)
app.include_router(billetes.router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}