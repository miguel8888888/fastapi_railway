"""
Inicializar base de datos completa con todas las tablas
"""

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

sys.path.append('.')

from app.database import engine, Base
from app.models.usuarios import Usuario
from app.models.pais import Pais
from app.models.billetes import Billete

def init_database():
    """
    Inicializa la base de datos con todas las tablas
    """
    print("🚀 Inicializando base de datos...")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    print("✅ Base de datos creada con éxito!")
    
    # Verificar que el archivo se creó
    if os.path.exists("app.db"):
        print(f"📋 Archivo de BD creado: app.db")
        
        # Mostrar información de las tablas
        import sqlite3
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"🏷️ Tablas creadas: {[table[0] for table in tables]}")
        
        conn.close()
    else:
        print("❌ No se encontró el archivo de BD")

if __name__ == "__main__":
    init_database()