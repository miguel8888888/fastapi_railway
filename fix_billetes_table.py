"""
Script simple y directo para agregar columnas a billetes en PostgreSQL
Ejecutar en el Shell de Render: python fix_billetes_table.py
"""

import os
import psycopg2
from psycopg2 import sql

def fix_billetes_table():
    """
    Agrega las columnas faltantes a la tabla billetes
    """
    print("🔧 REPARANDO TABLA BILLETES EN POSTGRESQL")
    print("=" * 50)
    
    # Obtener URL de la base de datos
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL no encontrada")
        return False
    
    print("🔗 Conectando a PostgreSQL...")
    
    try:
        # Conectar usando psycopg2 directamente
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexión establecida")
        
        # Verificar columnas actuales
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'billetes'
            ORDER BY ordinal_position
        """)
        columnas_actuales = [row[0] for row in cursor.fetchall()]
        print(f"📋 Columnas actuales ({len(columnas_actuales)}): {columnas_actuales}")
        
        # Definir las nuevas columnas
        nuevas_columnas = [
            ("banco_emisor", "VARCHAR(255)"),
            ("medidas", "VARCHAR(50)"),
            ("descripcion_anverso", "TEXT"),
            ("descripcion_reverso", "TEXT"),
            ("url_anverso", "TEXT"),
            ("url_reverso", "TEXT"),
            ("pick", "VARCHAR(50)"),
            ("estado", "VARCHAR(20) DEFAULT 'Bueno'"),
            ("vendido", "BOOLEAN DEFAULT false"),
            ("destacado", "BOOLEAN DEFAULT false"),
            ("fecha_actualizacion", "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP")
        ]
        
        print(f"\n🔄 Agregando {len(nuevas_columnas)} columnas nuevas...")
        
        columnas_agregadas = 0
        for nombre_columna, tipo_columna in nuevas_columnas:
            if nombre_columna not in columnas_actuales:
                try:
                    query = f"ALTER TABLE billetes ADD COLUMN {nombre_columna} {tipo_columna}"
                    print(f"➕ {nombre_columna}...")
                    cursor.execute(query)
                    print(f"✅ {nombre_columna} agregada")
                    columnas_agregadas += 1
                except Exception as e:
                    print(f"❌ Error agregando {nombre_columna}: {e}")
                    if "already exists" not in str(e):
                        conn.close()
                        return False
            else:
                print(f"✅ {nombre_columna} ya existe")
        
        # Migrar URLs
        print(f"\n🔄 Migrando URLs de imágenes...")
        cursor.execute("""
            UPDATE billetes 
            SET url_anverso = anverso, 
                url_reverso = reverso 
            WHERE (url_anverso IS NULL OR url_anverso = '') 
                AND anverso IS NOT NULL 
                AND anverso != ''
        """)
        filas_actualizadas = cursor.rowcount
        print(f"✅ {filas_actualizadas} filas actualizadas con URLs")
        
        # Crear índices
        print(f"\n🔄 Creando índices...")
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_billetes_pais ON billetes(pais)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_vendido ON billetes(vendido)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_destacado ON billetes(destacado)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_denominacion ON billetes(denominacion)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_pick ON billetes(pick)"
        ]
        
        for indice in indices:
            cursor.execute(indice)
        print(f"✅ {len(indices)} índices creados/verificados")
        
        # Verificar resultado final
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'billetes'
            ORDER BY ordinal_position
        """)
        columnas_finales = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📊 RESULTADO FINAL:")
        print(f"✅ Total columnas en billetes: {len(columnas_finales)}")
        print(f"✅ Columnas agregadas en esta ejecución: {columnas_agregadas}")
        print(f"📋 Columnas finales: {columnas_finales}")
        
        conn.close()
        
        print(f"\n🎉 ¡REPARACIÓN COMPLETADA EXITOSAMENTE!")
        print(f"🚀 Ahora puedes probar: https://fastapi-railway-ihky.onrender.com/billetes/")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        print(f"📋 Tipo de error: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = fix_billetes_table()
    exit(0 if success else 1)