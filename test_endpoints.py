"""
Script de prueba para verificar los nuevos endpoints de usuarios
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Probar los endpoints de usuarios"""
    
    print("🔍 Probando endpoints de usuarios...")
    
    # 1. Probar endpoint de lista de usuarios (sin autenticación para ver si existe)
    print("\n1. Probando GET /usuarios/")
    try:
        response = requests.get(f"{BASE_URL}/usuarios/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Endpoint existe pero requiere autenticación (correcto)")
        elif response.status_code == 404:
            print("   ❌ Endpoint no encontrado")
        else:
            print(f"   📋 Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Probar endpoint de búsqueda
    print("\n2. Probando GET /usuarios/?search=test")
    try:
        response = requests.get(f"{BASE_URL}/usuarios/?search=test")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Endpoint de búsqueda existe pero requiere autenticación (correcto)")
        elif response.status_code == 404:
            print("   ❌ Endpoint de búsqueda no encontrado")
        else:
            print(f"   📋 Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Probar endpoint de perfil
    print("\n3. Probando GET /auth/perfil/")
    try:
        response = requests.get(f"{BASE_URL}/auth/perfil/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Endpoint de perfil existe pero requiere autenticación (correcto)")
        elif response.status_code == 404:
            print("   ❌ Endpoint de perfil no encontrado")
        else:
            print(f"   📋 Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Obtener documentación de la API
    print("\n4. Obteniendo documentación OpenAPI")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            openapi = response.json()
            paths = openapi.get("paths", {})
            
            print("   📋 Endpoints encontrados:")
            for path in sorted(paths.keys()):
                if "/usuarios" in path or "/perfil" in path:
                    methods = list(paths[path].keys())
                    print(f"      {path} - {methods}")
        else:
            print(f"   ❌ No se pudo obtener documentación: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de endpoints...")
    test_endpoints()
    print("\n✅ Pruebas completadas")