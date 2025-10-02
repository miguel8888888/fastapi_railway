#!/usr/bin/env python3
"""
Script para corregir tipos de datos y relaciones en la base de datos de producción
EJECUTAR EN RENDER después del deployment
"""

import sys
import os
from sqlalchemy import text
from sqlalchemy.orm import Session

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal

def fix_production_database_schema():
    """Corrige el schema de la base de datos de producción"""
    
    db = SessionLocal()
    
    try:
        print("🔧 CORRIGIENDO SCHEMA DE BASE DE DATOS DE PRODUCCION")
        print("=" * 55)
        
        # Paso 1: Verificar estado actual
        print("1️⃣ Verificando estado actual...")
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'billetes' AND column_name = 'pais'
        """))
        for row in result:
            print(f"   - {row.column_name}: {row.data_type} (nullable: {row.is_nullable})")
        
        # Paso 2: Cambiar tipo de columna pais a INTEGER si es necesario
        print("\n2️⃣ Cambiando billetes.pais de VARCHAR a INTEGER...")
        try:
            # Verificar si ya es INTEGER
            result = db.execute(text("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name = 'billetes' AND column_name = 'pais'
            """)).fetchone()
            
            if result and result[0] != 'integer':
                db.execute(text("ALTER TABLE billetes ALTER COLUMN pais TYPE INTEGER USING pais::INTEGER;"))
                print("   ✅ Tipo de columna cambiado exitosamente")
            else:
                print("   ℹ️ La columna ya es de tipo INTEGER")
        except Exception as e:
            print(f"   ❌ Error al cambiar tipo: {e}")
        
        # Paso 3: Agregar foreign key constraint si no existe
        print("\n3️⃣ Verificando/agregando foreign key constraint...")
        try:
            # Verificar si la constraint ya existe
            result = db.execute(text("""
                SELECT conname 
                FROM pg_constraint 
                WHERE conrelid = 'billetes'::regclass 
                AND contype = 'f' 
                AND conname = 'fk_billetes_pais';
            """)).fetchone()
            
            if not result:
                # Eliminar constraint si existe con otro nombre
                db.execute(text("ALTER TABLE billetes DROP CONSTRAINT IF EXISTS fk_billetes_pais;"))
                
                # Agregar nueva constraint
                db.execute(text("""
                    ALTER TABLE billetes 
                    ADD CONSTRAINT fk_billetes_pais 
                    FOREIGN KEY (pais) REFERENCES paises(id);
                """))
                print("   ✅ Foreign key constraint agregada")
            else:
                print("   ℹ️ Foreign key constraint ya existe")
                
        except Exception as e:
            print(f"   ❌ Error en constraint: {e}")
        
        # Paso 4: Confirmar cambios
        db.commit()
        print("\n4️⃣ Cambios confirmados en la base de datos")
        
        # Paso 5: Verificar estado final
        print("\n5️⃣ Verificando estado final...")
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'billetes' AND column_name = 'pais'
        """))
        for row in result:
            print(f"   - {row.column_name}: {row.data_type} (nullable: {row.is_nullable})")
            
        # Verificar constraints
        result = db.execute(text("""
            SELECT conname, contype 
            FROM pg_constraint 
            WHERE conrelid = 'billetes'::regclass AND contype = 'f';
        """))
        constraints = list(result)
        if constraints:
            print("   - Foreign key constraints:")
            for constraint in constraints:
                print(f"     * {constraint.conname} (tipo: {constraint.contype})")
        else:
            print("   - ⚠️ No se encontraron foreign key constraints")
            
        print("\n🎉 SCHEMA CORREGIDO EXITOSAMENTE!")
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_production_database_schema()