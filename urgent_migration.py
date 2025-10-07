"""
Script de migración urgente para ejecutar directamente en Render Shell
"""

import os
import sys

def urgent_migration():
    """
    Ejecuta solo las alteraciones de tabla necesarias para la tabla billetes
    """
    print("🚨 MIGRACIÓN URGENTE - AGREGANDO COLUMNAS FALTANTES")
    print("=" * 60)
    
    # Importar después de verificar que estamos en el entorno correcto
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.orm import sessionmaker
    except ImportError as e:
        print(f"❌ Error importando SQLAlchemy: {e}")
        return False
    
    # Obtener URL de la base de datos
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL no encontrada en variables de entorno")
        return False
    
    print(f"🔗 Conectando a base de datos PostgreSQL...")
    
    try:
        # Crear conexión
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        with SessionLocal() as session:
            # Lista de columnas a agregar
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
            
            print(f"📋 Verificando columnas existentes...")
            
            # Verificar qué columnas ya existen
            result = session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'billetes'
            """))
            columnas_existentes = {row[0] for row in result}
            print(f"✅ Columnas existentes: {sorted(columnas_existentes)}")
            
            # Agregar columnas faltantes una por una
            columnas_agregadas = 0
            for columna, tipo in nuevas_columnas:
                if columna not in columnas_existentes:
                    try:
                        print(f"➕ Agregando columna '{columna}' ({tipo})...")
                        session.execute(text(f"ALTER TABLE billetes ADD COLUMN {columna} {tipo}"))
                        session.commit()
                        print(f"✅ Columna '{columna}' agregada exitosamente")
                        columnas_agregadas += 1
                    except Exception as e:
                        print(f"❌ Error agregando columna '{columna}': {e}")
                        session.rollback()
                        if "already exists" not in str(e).lower():
                            return False
                else:
                    print(f"✅ Columna '{columna}' ya existe")
            
            print(f"\n📊 RESULTADO:")
            print(f"✅ Columnas agregadas: {columnas_agregadas}")
            print(f"✅ Total columnas verificadas: {len(nuevas_columnas)}")
            
            # Verificar resultado final
            result = session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'billetes'
                ORDER BY column_name
            """))
            columnas_finales = [row[0] for row in result]
            print(f"✅ Columnas finales en billetes: {len(columnas_finales)}")
            
            # Migrar URLs si es necesario
            print(f"\n🔄 Migrando URLs de imágenes...")
            try:
                result = session.execute(text("""
                    UPDATE billetes 
                    SET url_anverso = anverso, 
                        url_reverso = reverso 
                    WHERE url_anverso IS NULL AND anverso IS NOT NULL
                """))
                session.commit()
                print(f"✅ URLs migradas: {result.rowcount} filas actualizadas")
            except Exception as e:
                print(f"⚠️ Error migrando URLs: {e}")
                session.rollback()
        
        print(f"\n🎉 ¡MIGRACIÓN URGENTE COMPLETADA!")
        print(f"🚀 Los endpoints de billetes deberían funcionar ahora")
        return True
        
    except Exception as e:
        print(f"❌ Error crítico durante la migración: {e}")
        print(f"📋 Detalles del error: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🔧 Iniciando migración urgente...")
    success = urgent_migration()
    
    if success:
        print("\n✅ MIGRACIÓN EXITOSA")
        print("🔗 Ahora puedes probar: https://fastapi-railway-ihky.onrender.com/billetes/")
        sys.exit(0)
    else:
        print("\n❌ MIGRACIÓN FALLÓ")
        print("📞 Contacta para debug manual")
        sys.exit(1)