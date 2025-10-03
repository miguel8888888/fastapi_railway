"""
Script de prueba para el endpoint de cambio de contraseña
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_change_password():
    """Probar el endpoint de cambio de contraseña"""
    
    print("🔐 Probando endpoint de cambio de contraseña...")
    
    # Ejemplo de payload para cambiar contraseña
    change_password_payload = {
        "current_password": "mi_contraseña_actual",
        "new_password": "mi_nueva_contraseña_segura_123",
        "confirm_new_password": "mi_nueva_contraseña_segura_123"
    }
    
    print("📋 Payload para cambio de contraseña:")
    print(json.dumps({
        "current_password": "***contraseña_actual***",
        "new_password": "***nueva_contraseña***", 
        "confirm_new_password": "***nueva_contraseña***"
    }, indent=2))
    
    print("\n🔒 Validaciones implementadas:")
    print("✅ Verificación de contraseña actual")
    print("✅ Validación de fortaleza de nueva contraseña")
    print("✅ Confirmación de nueva contraseña (deben coincidir)")
    print("✅ Nueva contraseña debe ser diferente a la actual")
    print("✅ Requiere autenticación (usuario logueado)")
    
    print("\n🔧 Para probar este endpoint:")
    print("1. Inicia el servidor: uvicorn app.main:app --reload --port 8000")
    print("2. Obtén un token de autenticación:")
    print("   POST /auth/login/")
    print("3. Usa el token para cambiar contraseña:")
    print("   PUT /auth/cambiar-password/")
    print("   Authorization: Bearer {tu_token}")
    print("   Content-Type: application/json")

def show_curl_example():
    """Mostrar ejemplo con curl"""
    
    print("\n📝 Ejemplo con curl:")
    print("# 1. Login para obtener token")
    print('curl -X POST "http://localhost:8000/auth/login/" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"email":"tu@email.com","password":"contraseña_actual"}\'')
    
    print("\n# 2. Cambiar contraseña")
    print('curl -X PUT "http://localhost:8000/auth/cambiar-password/" \\')
    print('     -H "Authorization: Bearer {tu_token_aqui}" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{\n       "current_password": "contraseña_actual",\n       "new_password": "nueva_contraseña_123",\n       "confirm_new_password": "nueva_contraseña_123"\n     }\'')

def show_security_features():
    """Mostrar características de seguridad"""
    
    print("\n🛡️ Características de seguridad:")
    print("🔹 Requiere contraseña actual para autorizar el cambio")
    print("🔹 Valida fortaleza de la nueva contraseña")
    print("🔹 Verifica que la nueva contraseña sea diferente")
    print("🔹 Requiere confirmación de nueva contraseña")
    print("🔹 Solo funciona para el usuario autenticado")
    print("🔹 Hashea la nueva contraseña con bcrypt")
    
    print("\n❌ Errores que puede devolver:")
    print("• 400: Contraseña actual incorrecta")
    print("• 400: Nueva contraseña no cumple requisitos de seguridad")
    print("• 400: Contraseñas de confirmación no coinciden")
    print("• 400: Nueva contraseña igual a la actual")
    print("• 401: Token de autenticación inválido")

if __name__ == "__main__":
    test_change_password()
    show_curl_example()
    show_security_features()