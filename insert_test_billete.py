"""
Script para insertar un nuevo billete de prueba
Usar después de la migración de la base de datos
"""

import requests
import json
from datetime import datetime

# Datos del nuevo billete
nuevo_billete = {
    "pais": 1,
    "denominacion": "50000",
    "precio": "150000",
    "banco_emisor": "Banco de la República de Colombia",
    "medidas": "70 x 140 mm",
    "descripcion_anverso": "Retrato de Gabriel García Márquez, escritor y premio Nobel de Literatura",
    "descripcion_reverso": "Escenas de Macondo y referencias a sus obras literarias",
    "url_anverso": "https://ljmwhelmcwtxbticvuwd.supabase.co/storage/v1/object/public/img-billetes/Reverso%2050%20mil.jpeg",
    "url_reverso": "https://ljmwhelmcwtxbticvuwd.supabase.co/storage/v1/object/public/img-billetes/Reverso%2050%20mil.jpeg",
    "pick": "P-458",
    "estado": "Excelente",
    "vendido": False,
    "destacado": True,
    "caracteristicas_ids": []
}

def insertar_billete_local():
    """Insertar en servidor local (desarrollo)"""
    url = "http://localhost:8000/billetes/"
    headers = {"Content-Type": "application/json"}
    
    print("🔗 Insertando billete en servidor LOCAL...")
    try:
        response = requests.post(url, json=nuevo_billete, headers=headers)
        if response.status_code == 201:
            print("✅ Billete insertado exitosamente en LOCAL")
            print(f"📋 ID asignado: {response.json().get('id')}")
            return response.json()
        else:
            print(f"❌ Error en LOCAL: {response.status_code}")
            print(f"📋 Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error conectando a LOCAL: {e}")
    return None

def insertar_billete_produccion():
    """Insertar en servidor de producción (Render)"""
    url = "https://fastapi-railway-ihky.onrender.com/billetes/"
    headers = {"Content-Type": "application/json"}
    
    print("🚀 Insertando billete en PRODUCCIÓN...")
    try:
        response = requests.post(url, json=nuevo_billete, headers=headers)
        if response.status_code == 201:
            print("✅ Billete insertado exitosamente en PRODUCCIÓN")
            print(f"📋 ID asignado: {response.json().get('id')}")
            return response.json()
        else:
            print(f"❌ Error en PRODUCCIÓN: {response.status_code}")
            print(f"📋 Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error conectando a PRODUCCIÓN: {e}")
    return None

def main():
    """Ejecutar inserción en ambos entornos"""
    print("💰 INSERTANDO NUEVO BILLETE DE 50.000 PESOS")
    print("=" * 50)
    print(f"🏦 Banco: {nuevo_billete['banco_emisor']}")
    print(f"💵 Denominación: ${nuevo_billete['denominacion']}")
    print(f"💰 Precio: ${nuevo_billete['precio']}")
    print(f"🌍 País ID: {nuevo_billete['pais']}")
    print(f"📏 Medidas: {nuevo_billete['medidas']}")
    print(f"🎯 Estado: {nuevo_billete['estado']}")
    print(f"⭐ Destacado: {'Sí' if nuevo_billete['destacado'] else 'No'}")
    print("=" * 50)
    
    # Intentar insertar en local
    resultado_local = insertar_billete_local()
    
    # Intentar insertar en producción
    resultado_produccion = insertar_billete_produccion()
    
    print("\n📊 RESUMEN:")
    print(f"🏠 Local: {'✅ Éxito' if resultado_local else '❌ Falló'}")
    print(f"🚀 Producción: {'✅ Éxito' if resultado_produccion else '❌ Falló'}")
    
    if resultado_produccion:
        print(f"\n🌐 Ver billete: https://fastapi-railway-ihky.onrender.com/billetes/{resultado_produccion['id']}")

if __name__ == "__main__":
    main()