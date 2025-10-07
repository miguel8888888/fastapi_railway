"""
Migración para sistema completo de billetes con características
Migra de la estructura actual a la nueva estructura completa
"""

import sqlite3
import os
from datetime import datetime

def migrate_billetes_system():
    """
    Migración completa del sistema de billetes
    """
    # Conexión a la base de datos
    db_path = "./app.db"
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada. Asegúrate de que app.db existe.")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔄 Iniciando migración del sistema de billetes...")
        
        # 1. Crear nueva tabla caracteristicas
        print("📋 1. Creando tabla 'caracteristicas'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS caracteristicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion TEXT,
            color VARCHAR(7) DEFAULT '#3B82F6',
            activo BOOLEAN DEFAULT TRUE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 2. Crear tabla de relación billete_caracteristicas
        print("📋 2. Creando tabla 'billete_caracteristicas'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS billete_caracteristicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            billete_id INTEGER REFERENCES billetes(id) ON DELETE CASCADE,
            caracteristica_id INTEGER REFERENCES caracteristicas(id) ON DELETE CASCADE,
            fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(billete_id, caracteristica_id)
        )
        """)
        
        # 3. Verificar estructura actual de billetes
        cursor.execute("PRAGMA table_info(billetes)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 3. Columnas actuales en billetes: {columns}")
        
        # 4. Agregar nuevas columnas a billetes si no existen
        new_columns = [
            ("banco_emisor", "VARCHAR(255)"),
            ("medidas", "VARCHAR(50)"),
            ("descripcion_anverso", "TEXT"),
            ("descripcion_reverso", "TEXT"),
            ("url_anverso", "TEXT"),
            ("url_reverso", "TEXT"),
            ("pick", "VARCHAR(50)"),
            ("estado", "VARCHAR(20)"),
            ("vendido", "BOOLEAN DEFAULT FALSE"),
            ("destacado", "BOOLEAN DEFAULT FALSE"),
            ("fecha_actualizacion", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                print(f"➕ Agregando columna '{column_name}'...")
                cursor.execute(f"ALTER TABLE billetes ADD COLUMN {column_name} {column_type}")
        
        # 5. Migrar datos existentes (anverso/reverso -> url_anverso/url_reverso)
        if 'anverso' in columns and 'url_anverso' in [col[0] for col in new_columns]:
            print("🔄 4. Migrando URLs de imágenes...")
            cursor.execute("""
            UPDATE billetes 
            SET url_anverso = anverso, url_reverso = reverso 
            WHERE (anverso IS NOT NULL AND anverso != '') 
               OR (reverso IS NOT NULL AND reverso != '')
            """)
        
        # 6. Insertar datos iniciales de características
        print("📋 5. Insertando características iniciales...")
        caracteristicas_iniciales = [
            ('Papel moneda', 'Billete impreso en papel tradicional', '#10B981'),
            ('Polímero', 'Billete de material plástico duradero', '#3B82F6'),
            ('Serie especial', 'Edición limitada o conmemorativa', '#F59E0B'),
            ('Sin circular', 'Billete en condición perfecta (UNC)', '#EF4444'),
            ('Marca de agua', 'Con marca de agua visible al trasluz', '#8B5CF6'),
            ('Holograma', 'Incluye elementos holográficos de seguridad', '#EC4899'),
            ('Microimpresión', 'Contiene texto microscópico de seguridad', '#6B7280'),
            ('Serie numerada', 'Billete con numeración específica', '#14B8A6'),
            ('Error de impresión', 'Billete con errores que lo hacen valioso', '#F97316'),
            ('Firma especial', 'Con firma de funcionario específico', '#84CC16')
        ]
        
        for nombre, descripcion, color in caracteristicas_iniciales:
            cursor.execute("""
            INSERT OR IGNORE INTO caracteristicas (nombre, descripcion, color)
            VALUES (?, ?, ?)
            """, (nombre, descripcion, color))
        
        # 7. Crear índices para optimización
        print("📋 6. Creando índices de optimización...")
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_billetes_pais ON billetes(pais)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_vendido ON billetes(vendido)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_destacado ON billetes(destacado)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_precio ON billetes(precio)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_denominacion ON billetes(denominacion)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_pick ON billetes(pick)",
            "CREATE INDEX IF NOT EXISTS idx_billetes_denominacion ON billetes(denominacion)",
            "CREATE INDEX IF NOT EXISTS idx_billete_caracteristicas_billete_id ON billete_caracteristicas(billete_id)",
            "CREATE INDEX IF NOT EXISTS idx_billete_caracteristicas_caracteristica_id ON billete_caracteristicas(caracteristica_id)"
        ]
        
        for index_sql in indices:
            cursor.execute(index_sql)
        
        # 8. Commit cambios
        conn.commit()
        print("✅ Migración completada exitosamente!")
        
        # 9. Mostrar estadísticas
        cursor.execute("SELECT COUNT(*) FROM billetes")
        billetes_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM caracteristicas")
        caracteristicas_count = cursor.fetchone()[0]
        
        print(f"\n📊 Estadísticas post-migración:")
        print(f"   📋 Billetes: {billetes_count}")
        print(f"   🏷️ Características: {caracteristicas_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 MIGRACIÓN DEL SISTEMA DE BILLETES")
    print("="*50)
    
    success = migrate_billetes_system()
    
    if success:
        print("\n✅ ¡Migración completada con éxito!")
        print("🎯 Próximos pasos:")
        print("   1. Verificar que los datos se migraron correctamente")
        print("   2. Actualizar los modelos SQLAlchemy")
        print("   3. Implementar los nuevos endpoints")
    else:
        print("\n❌ La migración falló. Revisa los errores arriba.")