"""
Completar migración del sistema de billetes
"""

import sqlite3
import sys
import os

def complete_migration():
    """
    Completa la migración agregando características e índices faltantes
    """
    print("🚀 COMPLETANDO MIGRACIÓN DEL SISTEMA DE BILLETES")
    print("=" * 50)
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        # 1. Verificar si ya existen características
        cursor.execute("SELECT COUNT(*) FROM caracteristicas")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📋 Insertando características iniciales...")
            
            caracteristicas = [
                ("Billete de Banco", "Billete emitido por un banco central", "#1f77b4"),
                ("Sin Circular", "Billete que nunca fue puesto en circulación", "#ff7f0e"),
                ("Plancha", "Billete en estado perfecto", "#2ca02c"),
                ("Especimen", "Billete de muestra sin valor legal", "#d62728"),
                ("Reemplazo", "Billete emitido para reemplazar otro dañado", "#9467bd"),
                ("Conmemorativo", "Billete emitido para conmemorar un evento especial", "#8c564b"),
                ("Polímero", "Billete fabricado en material polimérico", "#e377c2"),
                ("Papel", "Billete fabricado en papel algodón", "#7f7f7f"),
                ("Firma Única", "Billete con una combinación de firmas única", "#bcbd22"),
                ("Error de Impresión", "Billete con algún error durante la impresión", "#17becf")
            ]
            
            for nombre, descripcion, color in caracteristicas:
                cursor.execute("""
                INSERT INTO caracteristicas (nombre, descripcion, color)
                VALUES (?, ?, ?)
                """, (nombre, descripcion, color))
        else:
            print(f"✅ Ya existen {count} características")
        
        # 2. Crear índices de optimización
        print("📋 Creando índices de optimización...")
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_billetes_pais ON billetes(pais)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_vendido ON billetes(vendido)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_destacado ON billetes(destacado)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_precio ON billetes(precio)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_denominacion ON billetes(denominacion)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_pick ON billetes(pick)",
            "CREATE INDEX IF NOT EXISTS idx_billete_caracteristicas_billete_id ON billete_caracteristicas(billete_id)",
            "CREATE INDEX IF NOT EXISTS idx_billete_caracteristicas_caracteristica_id ON billete_caracteristicas(caracteristica_id)"
        ]
        
        for indice in indices:
            cursor.execute(indice)
        
        # 3. Migrar URLs de imágenes si es necesario
        print("🔄 Verificando migración de URLs...")
        cursor.execute("SELECT COUNT(*) FROM billetes WHERE url_anverso IS NULL AND anverso IS NOT NULL")
        count_null_urls = cursor.fetchone()[0]
        
        if count_null_urls > 0:
            print(f"📋 Migrando {count_null_urls} URLs de imágenes...")
            cursor.execute("""
                UPDATE billetes 
                SET url_anverso = anverso, 
                    url_reverso = reverso 
                WHERE url_anverso IS NULL AND anverso IS NOT NULL
            """)
        
        # 4. Verificar estructura final
        cursor.execute("PRAGMA table_info(billetes)")
        columnas_billetes = [col[1] for col in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(caracteristicas)")
        columnas_caracteristicas = [col[1] for col in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(billete_caracteristicas)")
        columnas_relacion = [col[1] for col in cursor.fetchall()]
        
        print(f"\n📊 RESUMEN DE LA MIGRACIÓN:")
        print(f"✅ Tabla billetes: {len(columnas_billetes)} columnas")
        print(f"✅ Tabla caracteristicas: {len(columnas_caracteristicas)} columnas")
        print(f"✅ Tabla billete_caracteristicas: {len(columnas_relacion)} columnas")
        
        # Confirmar cambios
        conn.commit()
        print("\n✅ ¡Migración completada exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    success = complete_migration()
    if not success:
        sys.exit(1)