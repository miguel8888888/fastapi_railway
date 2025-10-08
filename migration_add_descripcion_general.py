#!/usr/bin/env python3
"""
Script de migración para agregar columna descripcion_general a la tabla billetes
Ejecutar: python migration_add_descripcion_general.py
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import DATABASE_URL

def add_descripcion_general_column():
    """Agregar columna descripcion_general a la tabla billetes"""
    
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    
    # Verificar si la tabla billetes existe
    if 'billetes' not in inspector.get_table_names():
        print("❌ Error: La tabla 'billetes' no existe")
        return False
    
    # Verificar si la columna ya existe
    columns = [col['name'] for col in inspector.get_columns('billetes')]
    
    if 'descripcion_general' in columns:
        print("✅ La columna 'descripcion_general' ya existe en la tabla billetes")
        return True
    
    try:
        with engine.connect() as connection:
            # Agregar la nueva columna
            alter_query = text("""
                ALTER TABLE billetes 
                ADD COLUMN descripcion_general TEXT;
            """)
            
            connection.execute(alter_query)
            connection.commit()
            
            print("✅ Columna 'descripcion_general' agregada exitosamente a la tabla billetes")
            return True
            
    except Exception as e:
        print(f"❌ Error al agregar la columna: {str(e)}")
        return False
    
    finally:
        engine.dispose()

def main():
    """Función principal"""
    print("🔄 Iniciando migración para agregar columna 'descripcion_general'...")
    
    if add_descripcion_general_column():
        print("🎉 Migración completada exitosamente!")
    else:
        print("💥 Migración falló!")
        sys.exit(1)

if __name__ == "__main__":
    main()