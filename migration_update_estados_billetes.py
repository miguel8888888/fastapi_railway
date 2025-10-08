#!/usr/bin/env python3
"""
Script de migración para actualizar estados de billetes según nueva escala:
'Regular', 'Aceptable', 'Bueno', 'Muy bueno', 'Excelente'

Mapeo de estados antiguos a nuevos:
- 'Malo' → 'Regular'
- 'Regular' → 'Aceptable' 
- 'Bueno' → 'Bueno' (sin cambio)
- 'Excelente' → 'Excelente' (sin cambio)

Ejecutar: python migration_update_estados_billetes.py
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import DATABASE_URL

def update_estados_billetes():
    """Actualizar estados de billetes según nueva escala"""
    
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    
    # Verificar si la tabla billetes existe
    if 'billetes' not in inspector.get_table_names():
        print("❌ Error: La tabla 'billetes' no existe")
        return False
    
    try:
        with engine.connect() as connection:
            # Verificar estados actuales
            current_states_query = text("""
                SELECT DISTINCT estado, COUNT(*) as cantidad
                FROM billetes 
                WHERE estado IS NOT NULL
                GROUP BY estado
                ORDER BY estado;
            """)
            
            current_states = connection.execute(current_states_query).fetchall()
            
            print("🔍 Estados actuales en la base de datos:")
            for state, count in current_states:
                print(f"   - {state}: {count} billetes")
            
            # Mapear estados antiguos a nuevos
            estado_mapping = {
                'Malo': 'Regular',
                'Regular': 'Aceptable',
                'Bueno': 'Bueno',  # Sin cambio
                'Excelente': 'Excelente'  # Sin cambio
            }
            
            total_updated = 0
            
            for old_state, new_state in estado_mapping.items():
                if old_state != new_state:  # Solo actualizar si hay cambio
                    update_query = text("""
                        UPDATE billetes 
                        SET estado = :new_state 
                        WHERE estado = :old_state
                    """)
                    
                    result = connection.execute(update_query, {
                        'new_state': new_state,
                        'old_state': old_state
                    })
                    
                    updated_count = result.rowcount
                    total_updated += updated_count
                    
                    if updated_count > 0:
                        print(f"✅ Actualizado: '{old_state}' → '{new_state}' ({updated_count} billetes)")
            
            # Verificar estados finales
            final_states = connection.execute(current_states_query).fetchall()
            
            print("\n🎯 Estados finales en la base de datos:")
            for state, count in final_states:
                print(f"   - {state}: {count} billetes")
            
            connection.commit()
            
            print(f"\n✅ Migración completada: {total_updated} billetes actualizados")
            return True
            
    except Exception as e:
        print(f"❌ Error al actualizar estados: {str(e)}")
        return False
    
    finally:
        engine.dispose()

def main():
    """Función principal"""
    print("🔄 Iniciando migración de estados de billetes...")
    print("📋 Nueva escala: Regular < Aceptable < Bueno < Muy bueno < Excelente")
    
    if update_estados_billetes():
        print("🎉 Migración de estados completada exitosamente!")
    else:
        print("💥 Migración de estados falló!")
        sys.exit(1)

if __name__ == "__main__":
    main()