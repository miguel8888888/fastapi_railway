"""
Script para agregar billetes de prueba con las nuevas características
"""

import sys
import os
sys.path.append('.')

from app.database import SessionLocal
from app.models.billetes import Billete, Caracteristica
from app.models.pais import Pais

def create_sample_billetes():
    """
    Crea billetes de muestra con las nuevas características
    """
    print("🎯 CREANDO BILLETES DE MUESTRA")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # 1. Verificar que hay países disponibles
        paises = db.query(Pais).all()
        if not paises:
            print("❌ No hay países en la base de datos")
            return False
        
        # 2. Obtener características
        caracteristicas = db.query(Caracteristica).all()
        if not caracteristicas:
            print("❌ No hay características en la base de datos")
            return False
        
        print(f"✅ Encontrados {len(paises)} países y {len(caracteristicas)} características")
        
        # 3. Crear billetes de muestra
        billetes_muestra = [
            {
                "anverso": "billete_1_anverso.jpg",
                "reverso": "billete_1_reverso.jpg", 
                "pais": paises[0].id,
                "denominacion": "100 Pesos",
                "precio": "25.50",
                "banco_emisor": "Banco Central de la República",
                "medidas": "156 x 66 mm",
                "descripcion_anverso": "Retrato de José Martí con elementos patrióticos",
                "descripcion_reverso": "Paisaje nacional con flora típica",
                "pick": "P-125a",
                "estado": "Bueno",
                "vendido": False,
                "destacado": True,
                "caracteristicas_ids": [1, 3]  # Billete de Banco y Plancha
            },
            {
                "anverso": "billete_2_anverso.jpg",
                "reverso": "billete_2_reverso.jpg",
                "pais": paises[0].id if len(paises) > 0 else 1,
                "denominacion": "50 Dólares",
                "precio": "45.00",
                "banco_emisor": "Federal Reserve Bank",
                "medidas": "156 x 66 mm",
                "descripcion_anverso": "Benjamin Franklin con Independence Hall",
                "descripcion_reverso": "Independence Hall en Philadelphia",
                "pick": "P-540",
                "estado": "Excelente",
                "vendido": False,
                "destacado": True,
                "caracteristicas_ids": [2, 7]  # Sin Circular y Polímero
            },
            {
                "anverso": "billete_3_anverso.jpg",
                "reverso": "billete_3_reverso.jpg",
                "pais": paises[min(1, len(paises)-1)].id,
                "denominacion": "20 Euros",
                "precio": "15.75",
                "banco_emisor": "Banco Central Europeo",
                "medidas": "133 x 72 mm",
                "descripcion_anverso": "Arquitectura gótica europea",
                "descripcion_reverso": "Puente gótico con mapa de Europa",
                "pick": "P-21u",
                "estado": "Bueno",
                "vendido": True,
                "destacado": False,
                "caracteristicas_ids": [1, 8]  # Billete de Banco y Papel
            }
        ]
        
        for i, billete_data in enumerate(billetes_muestra, 1):
            print(f"\n📋 Creando billete {i}...")
            
            # Extraer IDs de características
            caracteristicas_ids = billete_data.pop('caracteristicas_ids', [])
            
            # Crear el billete
            billete = Billete(**billete_data)
            
            # Agregar características
            if caracteristicas_ids:
                caracteristicas_obj = db.query(Caracteristica).filter(
                    Caracteristica.id.in_(caracteristicas_ids)
                ).all()
                billete.caracteristicas = caracteristicas_obj
            
            db.add(billete)
            db.commit()
            db.refresh(billete)
            
            print(f"   ✅ Billete '{billete.denominacion}' creado (ID: {billete.id})")
            print(f"   - Banco: {billete.banco_emisor}")
            print(f"   - Pick: {billete.pick}")
            print(f"   - Estado: {billete.estado}")
            print(f"   - Características: {len(billete.caracteristicas)}")
        
        # 4. Verificar resultados
        total_billetes = db.query(Billete).count()
        billetes_destacados = db.query(Billete).filter(Billete.destacado == True).count()
        billetes_vendidos = db.query(Billete).filter(Billete.vendido == True).count()
        
        print(f"\n📊 RESUMEN:")
        print(f"✅ Total de billetes en BD: {total_billetes}")
        print(f"✅ Billetes destacados: {billetes_destacados}")
        print(f"✅ Billetes vendidos: {billetes_vendidos}")
        
    except Exception as e:
        print(f"❌ Error creando billetes de muestra: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    print(f"\n✅ ¡Billetes de muestra creados exitosamente!")
    return True

if __name__ == "__main__":
    success = create_sample_billetes()
    if not success:
        sys.exit(1)