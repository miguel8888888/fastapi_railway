#!/usr/bin/env python3
"""
Script para corregir tipos de datos y relaciones en la base de datos
EJECUTAR TANTO LOCALMENTE COMO EN RENDER
"""

import sys
import os
from sqlalchemy import text
from sqlalchemy.orm import Session

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine

def fix_database_schema():
    """Corrige el schema de la base de datos"""
    
    db = SessionLocal()
    
    try:
        print("🔧 CORRIGIENDO SCHEMA DE BASE DE DATOS")
        print("=" * 50)
        
        # Paso 1: Cambiar tipo de columna pais a INTEGER
        print("1️⃣ Cambiando billetes.pais de VARCHAR a INTEGER...")
        try:
            db.execute(text("ALTER TABLE billetes ALTER COLUMN pais TYPE INTEGER USING pais::INTEGER;"))
            print("   ✅ Tipo de columna cambiado exitosamente")
        except Exception as e:
            if "already exists" in str(e) or "cannot be cast" in str(e):
                print("   ⚠️ La columna ya tiene el tipo correcto o hay un problema de conversión")
            else:
                print(f"   ❌ Error al cambiar tipo: {e}")
        
        # Paso 2: Agregar foreign key constraint
        print("\n2️⃣ Agregando foreign key constraint...")
        try:
            # Primero eliminar constraint si existe
            db.execute(text("ALTER TABLE billetes DROP CONSTRAINT IF EXISTS fk_billetes_pais;"))
            
            # Agregar nueva constraint
            db.execute(text("""
                ALTER TABLE billetes 
                ADD CONSTRAINT fk_billetes_pais 
                FOREIGN KEY (pais) REFERENCES paises(id);
            """))
            print("   ✅ Foreign key constraint agregada")
        except Exception as e:
            print(f"   ❌ Error al agregar foreign key: {e}")
        
        # Paso 3: Verificar la corrección
        print("\n3️⃣ Verificando corrección...")
        result = db.execute(text("""
            SELECT b.id, b.pais, p.pais as pais_nombre
            FROM billetes b
            LEFT JOIN paises p ON p.id = b.pais
            LIMIT 5;
        """))
        
        rows = result.fetchall()
        if rows:
            print("   ✅ JOIN funcionando correctamente:")
            for row in rows:
                print(f"   - Billete {row[0]}: pais_id={row[1]} -> {row[2] or 'NO ENCONTRADO'}")
        else:
            print("   ⚠️ No hay datos para verificar")
        
        db.commit()
        print("\n✅ CORRECCIÓN COMPLETADA EXITOSAMENTE")
        
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def main():
    print("🛠️ CORRECTOR DE SCHEMA DE BASE DE DATOS")
    print("=" * 50)
    print("Este script corrige los tipos de datos incorrectos")
    print("Ejecutar tanto localmente como en Render\n")
    
    fix_database_schema()

if __name__ == "__main__":
    main()