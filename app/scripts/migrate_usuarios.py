"""
Script para migrar la base de datos y agregar los nuevos campos a la tabla usuarios
"""

from sqlalchemy import text
from app.database import engine, SessionLocal

def migrate_usuarios_table():
    """
    Agregar nuevos campos a la tabla usuarios existente
    """
    
    # Comandos SQL para agregar las nuevas columnas
    migrations = [
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS telefono VARCHAR(20)",
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS ciudad VARCHAR(100)",
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS direccion VARCHAR(500)",
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS pais VARCHAR(100)"
    ]
    
    db = SessionLocal()
    
    try:
        print("🔄 Iniciando migración de tabla usuarios...")
        
        for migration in migrations:
            try:
                db.execute(text(migration))
                column_name = migration.split("ADD COLUMN IF NOT EXISTS ")[1].split(" ")[0]
                print(f"✅ Columna agregada: {column_name}")
            except Exception as e:
                if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                    column_name = migration.split("ADD COLUMN IF NOT EXISTS ")[1].split(" ")[0]
                    print(f"⚠️  Columna ya existe: {column_name}")
                else:
                    print(f"❌ Error en: {migration}")
                    print(f"   Error: {e}")
        
        db.commit()
        print("\n✅ Migración completada exitosamente")
        print("📋 Nuevos campos agregados a la tabla usuarios:")
        print("   - telefono (VARCHAR(20))")
        print("   - ciudad (VARCHAR(100))")
        print("   - direccion (VARCHAR(500))")
        print("   - pais (VARCHAR(100))")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error en la migración: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    migrate_usuarios_table()