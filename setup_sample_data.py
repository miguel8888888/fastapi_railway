"""
Verificar y crear países de muestra
"""

import sqlite3
import sys
import os

def setup_sample_data():
    """
    Verifica y crea datos de muestra necesarios
    """
    print("🔧 CONFIGURANDO DATOS DE MUESTRA")
    print("=" * 50)
    
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    try:
        # Verificar tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"📋 Tablas encontradas: {tables}")
        
        # Verificar países
        if 'paises' in tables:
            cursor.execute("SELECT COUNT(*) FROM paises")
            count_paises = cursor.fetchone()[0]
            print(f"📊 Países existentes: {count_paises}")
            
            if count_paises == 0:
                print("📝 Creando países de muestra...")
                paises_muestra = [
                    ("Argentina", "🇦🇷"),
                    ("Estados Unidos", "🇺🇸"),
                    ("España", "🇪🇸"),
                    ("México", "🇲🇽"),
                    ("Brasil", "🇧🇷")
                ]
                
                for pais, bandera in paises_muestra:
                    cursor.execute("INSERT INTO paises (pais, bandera) VALUES (?, ?)", (pais, bandera))
                
                conn.commit()
                print(f"✅ Creados {len(paises_muestra)} países")
        
        # Verificar características
        cursor.execute("SELECT COUNT(*) FROM caracteristicas")
        count_caracteristicas = cursor.fetchone()[0]
        print(f"📊 Características existentes: {count_caracteristicas}")
        
        # Verificar billetes
        cursor.execute("SELECT COUNT(*) FROM billetes")
        count_billetes = cursor.fetchone()[0]
        print(f"📊 Billetes existentes: {count_billetes}")
        
        # Mostrar algunos ejemplos de países si existen
        if 'paises' in tables:
            cursor.execute("SELECT id, pais FROM paises LIMIT 5")
            paises_ejemplo = cursor.fetchall()
            print(f"🌍 Ejemplos de países:")
            for pais_id, pais_nombre in paises_ejemplo:
                print(f"   - ID: {pais_id}, Nombre: {pais_nombre}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    success = setup_sample_data()
    if not success:
        sys.exit(1)