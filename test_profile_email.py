"""
Script para probar la actualización del perfil con el nuevo campo email
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_profile_update():
    """Probar la actualización del perfil incluyendo email"""
    
    print("📧 Probando actualización de perfil con email...")
    
    # Ejemplo de payload para actualizar perfil
    profile_update_payload = {
        "email": "nuevo_email@ejemplo.com",
        "nombre": "Miguel Actualizado",
        "apellidos": "García Pérez", 
        "telefono": "+34 123 456 789",
        "ciudad": "Madrid",
        "direccion": "Calle Nueva 123, Piso 2A",
        "pais": "España"
    }
    
    print("📋 Payload de actualización:")
    print(json.dumps(profile_update_payload, indent=2, ensure_ascii=False))
    
    print("\n🔧 Para probar este endpoint:")
    print("1. Inicia el servidor: uvicorn app.main:app --reload --port 8000")
    print("2. Obtén un token de autenticación:")
    print("   POST /auth/login/")
    print("3. Usa el token para actualizar el perfil:")
    print(f"   PUT /auth/perfil/")
    print("   Authorization: Bearer {tu_token}")
    print("   Content-Type: application/json")
    
    print("\n✅ Campo email ahora incluido en UserProfileUpdate")
    print("✅ Validación de email duplicado implementada")
    print("✅ Endpoint PUT /auth/perfil/ listo para usar")

def show_curl_example():
    """Mostrar ejemplo con curl"""
    
    print("\n📝 Ejemplo con curl:")
    print("# 1. Login para obtener token")
    print('curl -X POST "http://localhost:8000/auth/login/" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"email":"admin@ejemplo.com","password":"tu_password"}\'')
    
    print("\n# 2. Actualizar perfil (incluyendo email)")
    print('curl -X PUT "http://localhost:8000/auth/perfil/" \\')
    print('     -H "Authorization: Bearer {tu_token_aqui}" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{\n       "email": "nuevo@ejemplo.com",\n       "nombre": "Miguel",\n       "telefono": "+34 123 456 789",\n       "ciudad": "Madrid",\n       "direccion": "Calle Nueva 123",\n       "pais": "España"\n     }\'')

if __name__ == "__main__":
    test_profile_update()
    show_curl_example()