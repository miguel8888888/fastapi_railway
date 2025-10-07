"""
Script para insertar billete usando SQL directo en PostgreSQL
Ya que los endpoints requieren autenticación
"""

import os
import psycopg2
from psycopg2 import sql
from datetime import datetime

def insertar_billete_sql():
    """
    Inserta un nuevo billete directamente en PostgreSQL
    """
    print("🔧 INSERTANDO BILLETE DIRECTO EN POSTGRESQL")
    print("=" * 50)
    
    # Datos del billete
    billete_data = {
        'pais': 1,
        'denominacion': '50000',
        'precio': '150000',
        'banco_emisor': 'Banco de la República de Colombia',
        'medidas': '70 x 140 mm',
        'descripcion_anverso': 'Retrato de Gabriel García Márquez, escritor y premio Nobel de Literatura',
        'descripcion_reverso': 'Escenas de Macondo y referencias a sus obras literarias',
        'url_anverso': 'https://ljmwhelmcwtxbticvuwd.supabase.co/storage/v1/object/public/img-billetes/Reverso%2050%20mil.jpeg',
        'url_reverso': 'https://ljmwhelmcwtxbticvuwd.supabase.co/storage/v1/object/public/img-billetes/Reverso%2050%20mil.jpeg',
        'pick': 'P-458',
        'estado': 'Excelente',
        'vendido': False,
        'destacado': True
    }
    
    print("💰 DATOS DEL BILLETE:")
    for key, value in billete_data.items():
        print(f"   {key}: {value}")
    print("=" * 50)
    
    # Obtener URL de la base de datos (solo funcionará en producción)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL no encontrada")
        print("💡 Este script debe ejecutarse en el entorno de producción (Render)")
        return False
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexión establecida con PostgreSQL")
        
        # SQL para insertar el billete
        insert_query = """
        INSERT INTO billetes (
            pais, denominacion, precio, banco_emisor, medidas,
            descripcion_anverso, descripcion_reverso, 
            url_anverso, url_reverso, pick, estado, vendido, destacado,
            fecha_actualizacion
        ) VALUES (
            %(pais)s, %(denominacion)s, %(precio)s, %(banco_emisor)s, %(medidas)s,
            %(descripcion_anverso)s, %(descripcion_reverso)s,
            %(url_anverso)s, %(url_reverso)s, %(pick)s, %(estado)s, %(vendido)s, %(destacado)s,
            CURRENT_TIMESTAMP
        ) RETURNING id, fecha_actualizacion;
        """
        
        print("📝 Ejecutando INSERT...")
        cursor.execute(insert_query, billete_data)
        
        # Obtener el ID del billete insertado
        result = cursor.fetchone()
        billete_id, fecha_creacion = result
        
        print(f"✅ ¡Billete insertado exitosamente!")
        print(f"🆔 ID asignado: {billete_id}")
        print(f"📅 Fecha de creación: {fecha_creacion}")
        
        # Verificar el billete insertado
        cursor.execute("SELECT * FROM billetes WHERE id = %s", (billete_id,))
        billete_verificado = cursor.fetchone()
        
        print(f"\n📋 BILLETE VERIFICADO:")
        print(f"   ID: {billete_verificado[0]}")
        print(f"   País: {billete_verificado[1]}")
        print(f"   Denominación: ${billete_verificado[2]}")
        print(f"   Precio: ${billete_verificado[3]}")
        print(f"   Estado: {billete_verificado[10]}")
        
        conn.close()
        
        print(f"\n🌐 Puedes ver el billete en:")
        print(f"   https://fastapi-railway-ihky.onrender.com/billetes/{billete_id}")
        print(f"   https://fastapi-railway-ihky.onrender.com/billetes/")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = insertar_billete_sql()
    exit(0 if success else 1)