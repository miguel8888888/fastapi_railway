#!/usr/bin/env python3
"""
Script para verificar y corregir tipos de datos en la base de datos
Especialmente la relación billetes.pais -> paises.id
"""

import sys
import os
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine

def check_table_structure():
    """Verifica la estructura actual de las tablas"""
    
    db = SessionLocal()
    inspector = inspect(engine)
    
    try:
        print("🔍 Verificando estructura de las tablas...")
        print("=" * 60)
        
        # Verificar tabla paises
        print("\n📋 TABLA 'paises':")
        paises_columns = inspector.get_columns('paises')
        for col in paises_columns:
            print(f"   - {col['name']}: {col['type']} (nullable: {col['nullable']})")
        
        # Verificar tabla billetes
        print("\n💵 TABLA 'billetes':")
        billetes_columns = inspector.get_columns('billetes')
        for col in billetes_columns:
            print(f"   - {col['name']}: {col['type']} (nullable: {col['nullable']})")
            
        # Verificar foreign keys
        print("\n🔗 FOREIGN KEYS en 'billetes':")
        fks = inspector.get_foreign_keys('billetes')
        for fk in fks:
            print(f"   - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        # Verificar datos problemáticos
        print("\n🔍 Verificando datos en billetes.pais...")
        result = db.execute(text("SELECT pais, COUNT(*) as count FROM billetes GROUP BY pais LIMIT 10"))
        rows = result.fetchall()
        
        if rows:
            print("   Valores en billetes.pais:")
            for row in rows:
                print(f"   - '{row[0]}' (tipo: {type(row[0]).__name__}) -> {row[1]} registros")
        
        # Verificar si hay problemas de conversión
        print("\n⚠️ Verificando problemas de tipo...")
        try:
            problem_query = text("""
                SELECT b.id, b.pais, p.id as pais_id, p.pais as pais_nombre
                FROM billetes b
                LEFT JOIN paises p ON CAST(b.pais AS INTEGER) = p.id
                LIMIT 5
            """)
            result = db.execute(problem_query)
            test_rows = result.fetchall()
            print("   ✅ La conversión CAST funciona correctamente")
            
            for row in test_rows:
                print(f"   - Billete {row[0]}: pais='{row[1]}' -> {row[3] or 'NO ENCONTRADO'}")
                
        except Exception as e:
            print(f"   ❌ Error en conversión: {e}")
        
    except Exception as e:
        print(f"❌ Error al verificar estructura: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def fix_billetes_pais_type():
    """Intenta corregir el tipo de datos de billetes.pais"""
    
    db = SessionLocal()
    
    try:
        print("\n🛠️ Intentando corregir tipo de datos...")
        print("=" * 60)
        
        # Verificar si podemos convertir todos los valores
        print("1. Verificando que todos los valores sean convertibles a INTEGER...")
        
        check_query = text("""
            SELECT pais, COUNT(*) 
            FROM billetes 
            WHERE pais !~ '^[0-9]+$'
            GROUP BY pais
        """)
        
        result = db.execute(check_query)
        invalid_values = result.fetchall()
        
        if invalid_values:
            print("   ❌ Valores no convertibles encontrados:")
            for row in invalid_values:
                print(f"   - '{row[0]}' -> {row[1]} registros")
            return False
        else:
            print("   ✅ Todos los valores son convertibles a INTEGER")
        
        # Mostrar el comando SQL para corregir manualmente
        print("\n2. 📝 SQL para corregir en producción:")
        print("   Ejecuta esto en la consola de PostgreSQL de Render:")
        print("")
        print("   -- Paso 1: Cambiar tipo de columna")
        print("   ALTER TABLE billetes ALTER COLUMN pais TYPE INTEGER USING pais::INTEGER;")
        print("")
        print("   -- Paso 2: Verificar la corrección")
        print("   SELECT b.id, b.pais, p.pais as pais_nombre")
        print("   FROM billetes b")
        print("   LEFT JOIN paises p ON p.id = b.pais")
        print("   LIMIT 5;")
        print("")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar corrección: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

def main():
    print("🔧 VERIFICADOR Y CORRECTOR DE TIPOS DE DATOS")
    print("=" * 60)
    
    check_table_structure()
    fix_billetes_pais_type()
    
    print("\n" + "=" * 60)
    print("✅ Verificación completada")
    print("💡 Si ves errores de tipo, ejecuta el SQL mostrado en Render")

if __name__ == "__main__":
    main()