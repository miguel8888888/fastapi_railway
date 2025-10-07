"""
Script de migración para producción en Render
Este script ejecuta las migraciones necesarias para el sistema de billetes
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_production():
    """
    Ejecuta la migración en la base de datos de producción
    """
    logger.info("🚀 INICIANDO MIGRACIÓN DE PRODUCCIÓN")
    logger.info("=" * 50)
    
    # Obtener URL de la base de datos
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        logger.error("❌ DATABASE_URL no encontrada en variables de entorno")
        return False
    
    logger.info(f"🔗 Conectando a base de datos...")
    
    try:
        # Crear conexión
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        with SessionLocal() as session:
            # 1. Verificar si ya existe la tabla caracteristicas
            result = session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'caracteristicas'
                )
            """))
            caracteristicas_exists = result.scalar()
            
            if not caracteristicas_exists:
                logger.info("📋 Creando tabla 'caracteristicas'...")
                session.execute(text("""
                    CREATE TABLE caracteristicas (
                        id SERIAL PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL UNIQUE,
                        descripcion TEXT,
                        color VARCHAR(7) DEFAULT '#007bff',
                        activo BOOLEAN DEFAULT true,
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                session.commit()
                logger.info("✅ Tabla 'caracteristicas' creada")
            else:
                logger.info("✅ Tabla 'caracteristicas' ya existe")
            
            # 2. Verificar si ya existe la tabla billete_caracteristicas
            result = session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'billete_caracteristicas'
                )
            """))
            relacion_exists = result.scalar()
            
            if not relacion_exists:
                logger.info("📋 Creando tabla 'billete_caracteristicas'...")
                session.execute(text("""
                    CREATE TABLE billete_caracteristicas (
                        id SERIAL PRIMARY KEY,
                        billete_id INTEGER NOT NULL,
                        caracteristica_id INTEGER NOT NULL,
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (billete_id) REFERENCES billetes(id) ON DELETE CASCADE,
                        FOREIGN KEY (caracteristica_id) REFERENCES caracteristicas(id) ON DELETE CASCADE,
                        UNIQUE(billete_id, caracteristica_id)
                    )
                """))
                session.commit()
                logger.info("✅ Tabla 'billete_caracteristicas' creada")
            else:
                logger.info("✅ Tabla 'billete_caracteristicas' ya existe")
            
            # 3. Agregar columnas faltantes a la tabla billetes
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
            
            for columna, tipo in nuevas_columnas:
                try:
                    logger.info(f"➕ Agregando columna '{columna}'...")
                    session.execute(text(f"ALTER TABLE billetes ADD COLUMN {columna} {tipo}"))
                    session.commit()
                    logger.info(f"✅ Columna '{columna}' agregada")
                except Exception as e:
                    if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                        logger.info(f"✅ Columna '{columna}' ya existe")
                    else:
                        logger.warning(f"⚠️ Error agregando columna '{columna}': {e}")
                        session.rollback()
            
            # 4. Insertar características iniciales si no existen
            result = session.execute(text("SELECT COUNT(*) FROM caracteristicas"))
            count = result.scalar()
            
            if count == 0:
                logger.info("📋 Insertando características iniciales...")
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
                    session.execute(text("""
                        INSERT INTO caracteristicas (nombre, descripcion, color)
                        VALUES (:nombre, :descripcion, :color)
                    """), {"nombre": nombre, "descripcion": descripcion, "color": color})
                
                session.commit()
                logger.info(f"✅ Insertadas {len(caracteristicas)} características")
            else:
                logger.info(f"✅ Ya existen {count} características")
            
            # 5. Crear índices para optimización
            logger.info("📋 Creando índices de optimización...")
            indices = [
                "CREATE INDEX IF NOT EXISTS idx_billetes_pais ON billetes(pais)",
                "CREATE INDEX IF NOT EXISTS idx_billetes_vendido ON billetes(vendido)",
                "CREATE INDEX IF NOT EXISTS idx_billetes_destacado ON billetes(destacado)",
                "CREATE INDEX IF NOT EXISTS idx_billetes_denominacion ON billetes(denominacion)",
                "CREATE INDEX IF NOT EXISTS idx_billetes_pick ON billetes(pick)",
                "CREATE INDEX IF NOT EXISTS idx_billete_caracteristicas_billete_id ON billete_caracteristicas(billete_id)",
                "CREATE INDEX IF NOT EXISTS idx_billete_caracteristicas_caracteristica_id ON billete_caracteristicas(caracteristica_id)"
            ]
            
            for indice in indices:
                try:
                    session.execute(text(indice))
                    session.commit()
                except Exception as e:
                    logger.warning(f"⚠️ Error creando índice: {e}")
                    session.rollback()
            
            logger.info("✅ Índices creados")
            
            # 6. Migrar URLs de imágenes existentes si es necesario
            result = session.execute(text("""
                SELECT COUNT(*) FROM billetes 
                WHERE url_anverso IS NULL AND anverso IS NOT NULL
            """))
            count_null_urls = result.scalar()
            
            if count_null_urls > 0:
                logger.info(f"📋 Migrando {count_null_urls} URLs de imágenes...")
                session.execute(text("""
                    UPDATE billetes 
                    SET url_anverso = anverso, 
                        url_reverso = reverso 
                    WHERE url_anverso IS NULL AND anverso IS NOT NULL
                """))
                session.commit()
                logger.info("✅ URLs migradas")
        
        logger.info("\n✅ ¡MIGRACIÓN DE PRODUCCIÓN COMPLETADA EXITOSAMENTE!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error durante la migración: {e}")
        return False

if __name__ == "__main__":
    success = migrate_production()
    if not success:
        sys.exit(1)