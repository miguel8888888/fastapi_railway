"""
Pruebas de los nuevos endpoints del sistema de billetes
"""

import sys
import os
sys.path.append('.')

from app.database import SessionLocal
from app.crud.billetes import get_caracteristicas, get_billetes_stats
from app.models.billetes import Caracteristica

def test_endpoints():
    """
    Prueba las nuevas funcionalidades del sistema de billetes
    """
    print("🧪 PROBANDO SISTEMA DE BILLETES")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # 1. Probar características
        print("\n📋 1. Probando características...")
        caracteristicas = get_caracteristicas(db)
        print(f"✅ Encontradas {len(caracteristicas)} características:")
        for carac in caracteristicas[:5]:  # Mostrar solo las primeras 5
            print(f"   - {carac.nombre} ({carac.color})")
        
        # 2. Probar estadísticas
        print("\n📊 2. Probando estadísticas...")
        stats = get_billetes_stats(db)
        print(f"✅ Estadísticas:")
        print(f"   - Total billetes: {stats['total_billetes']}")
        print(f"   - Vendidos: {stats['total_vendidos']}")
        print(f"   - Disponibles: {stats['total_disponibles']}")
        print(f"   - Destacados: {stats['total_destacados']}")
        print(f"   - Valor total: ${stats['valor_total_inventario']}")
        
        # 3. Verificar estructura de la base de datos
        print("\n🗄️ 3. Verificando estructura de la BD...")
        import sqlite3
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        # Verificar columnas de billetes
        cursor.execute("PRAGMA table_info(billetes)")
        columnas_billetes = [col[1] for col in cursor.fetchall()]
        nuevas_columnas = ['banco_emisor', 'medidas', 'descripcion_anverso', 'descripcion_reverso', 
                          'url_anverso', 'url_reverso', 'pick', 'estado', 'vendido', 'destacado']
        
        print(f"✅ Billetes tiene {len(columnas_billetes)} columnas")
        for col in nuevas_columnas:
            if col in columnas_billetes:
                print(f"   ✅ {col}")
            else:
                print(f"   ❌ {col} (faltante)")
        
        # Verificar tabla caracteristicas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='caracteristicas'")
        if cursor.fetchone():
            print(f"✅ Tabla 'caracteristicas' existe")
            cursor.execute("SELECT COUNT(*) FROM caracteristicas")
            count = cursor.fetchone()[0]
            print(f"   - Contiene {count} registros")
        else:
            print(f"❌ Tabla 'caracteristicas' no existe")
        
        # Verificar tabla billete_caracteristicas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='billete_caracteristicas'")
        if cursor.fetchone():
            print(f"✅ Tabla 'billete_caracteristicas' existe")
        else:
            print(f"❌ Tabla 'billete_caracteristicas' no existe")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        return False
    finally:
        db.close()
    
    print(f"\n✅ ¡Pruebas completadas!")
    return True

if __name__ == "__main__":
    success = test_endpoints()
    if not success:
        sys.exit(1)