"""
Prueba rápida del email con las configuraciones corregidas
"""

import os
import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

from app.utils.email_service import send_reset_email

def test_email():
    print("🧪 Prueba de Email de Recuperación")
    print("="*50)
    
    # Verificar configuración
    frontend_url = os.getenv("FRONTEND_URL")
    print(f"✅ FRONTEND_URL: {frontend_url}")
    
    if "numismatica.onrender.com" not in str(frontend_url):
        print("⚠️  URL no es la esperada!")
        return
    
    # Probar envío
    print("\n🚀 Enviando email de prueba...")
    
    try:
        result = send_reset_email(
            email="miguelsgap@gmail.com",
            token="TEST_TOKEN_12345",
            nombre="Administrador Prueba"
        )
        
        if result:
            print("✅ Email enviado exitosamente!")
            print("📧 Revisa tu bandeja de entrada")
            print("🔍 Verifica que la URL sea: https://numismatica.onrender.com/auth/reset-password?token=TEST_TOKEN_12345")
        else:
            print("❌ Error enviando email")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_email()