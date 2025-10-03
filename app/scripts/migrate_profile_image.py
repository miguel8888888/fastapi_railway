"""
Script para migrar la base de datos y agregar los campos de imagen de perfil
"""

from sqlalchemy import text
from app.database import engine, SessionLocal

def migrate_profile_image_fields():
    """
    Agregar campos de imagen de perfil a la tabla usuarios
    """
    
    # Comandos SQL para agregar las nuevas columnas
    migrations = [
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS profile_image VARCHAR(500)",
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS profile_image_path VARCHAR(300)"
    ]
    
    db = SessionLocal()
    
    try:
        print("🔄 Iniciando migración de campos de imagen de perfil...")
        
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
        print("📋 Nuevos campos agregados para imagen de perfil:")
        print("   - profile_image (VARCHAR(500)) - URL pública de Supabase")
        print("   - profile_image_path (VARCHAR(300)) - Ruta interna para eliminar")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error en la migración: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    migrate_profile_image_fields()