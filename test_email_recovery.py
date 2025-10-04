"""
Script de prueba para verificar el envío de email de recuperación
Verificará que use la URL correcta: https://numismatica.onrender.com
"""

import requests
import json
import os
import sys

# Configurar la URL base de la API
API_BASE_URL = "http://127.0.0.1:8000"

def test_forgot_password_email():
    """
    Prueba el endpoint de forgot password para verificar la URL correcta
    """
    
    # Email de prueba (debe existir en la base de datos)
    test_email = "miguelsgap@gmail.com"  # Reemplaza con un email real de tu DB
    
    # Endpoint de forgot password
    url = f"{API_BASE_URL}/auth/forgot-password/"
    
    # Datos de la request
    data = {
        "email": test_email
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"🧪 Probando recuperación de contraseña para: {test_email}")
        print(f"📡 Enviando POST a: {url}")
        print(f"📊 Datos: {json.dumps(data, indent=2)}")
        print("\n" + "="*50)
        
        # Enviar request
        response = requests.post(
            url,
            json=data,
            headers=headers,
            timeout=30
        )
        
        print(f"📋 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Request exitosa!")
            print("📧 Revisa tu email y los logs del servidor para verificar:")
            print("   1. Que la URL sea: https://numismatica.onrender.com/auth/reset-password?token=...")
            print("   2. Que aparezca el botón de 'Restablecer Contraseña'")
        else:
            print(f"\n❌ Error en la request: {response.status_code}")
            print(f"   Mensaje: {response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Asegúrate de que el servidor esté corriendo en http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_environment_variables():
    """
    Verifica que las variables de entorno estén configuradas correctamente
    """
    
    print("🔧 Verificando variables de entorno...")
    print("="*50)
    
    # Cargar variables de entorno desde .env
    from dotenv import load_dotenv
    load_dotenv()
    
    # Variables importantes
    variables = {
        "FRONTEND_URL": os.getenv("FRONTEND_URL"),
        "EMAILJS_SERVICE_ID": os.getenv("EMAILJS_SERVICE_ID"),
        "EMAILJS_TEMPLATE_ID": os.getenv("EMAILJS_TEMPLATE_ID"),
        "EMAILJS_PUBLIC_KEY": os.getenv("EMAILJS_PUBLIC_KEY"),
        "EMAIL_USER": os.getenv("EMAIL_USER"),
    }
    
    for var_name, var_value in variables.items():
        if var_value:
            if "KEY" in var_name or "PASSWORD" in var_name:
                # Mostrar solo los primeros y últimos caracteres por seguridad
                masked_value = f"{var_value[:4]}...{var_value[-4:]}" if len(var_value) > 8 else "***"
                print(f"✅ {var_name}: {masked_value}")
            else:
                print(f"✅ {var_name}: {var_value}")
        else:
            print(f"❌ {var_name}: No configurada")
    
    print("\n" + "="*50)
    
    # Verificar específicamente FRONTEND_URL
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url == "https://numismatica.onrender.com":
        print("✅ FRONTEND_URL está configurada correctamente!")
    elif frontend_url == "http://localhost:4200":
        print("⚠️  FRONTEND_URL todavía apunta a localhost")
        print("   Asegúrate de reiniciar el servidor después de cambiar .env")
    else:
        print(f"⚠️  FRONTEND_URL tiene un valor inesperado: {frontend_url}")

if __name__ == "__main__":
    print("🚀 Script de Prueba - Email de Recuperación")
    print("="*60)
    
    # Verificar variables de entorno primero
    test_environment_variables()
    
    print("\n" + "="*60)
    
    # Preguntar si continuar con la prueba de email
    user_input = input("\n¿Quieres enviar un email de prueba? (s/n): ").lower().strip()
    
    if user_input in ['s', 'si', 'y', 'yes']:
        # Preguntar por el email si no es el por defecto
        custom_email = input("\n📧 Email para la prueba (Enter para usar miguelsgap@gmail.com): ").strip()
        if custom_email:
            # Actualizar el email de prueba
            print(f"📧 Usando email personalizado: {custom_email}")
        
        test_forgot_password_email()
    else:
        print("✅ Prueba cancelada. Variables de entorno verificadas.")