#!/usr/bin/env python3
"""
Script para probar la configuración de Gmail SMTP
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))

from app.utils.email_service import test_email_configuration, send_reset_email
from dotenv import load_dotenv

def main():
    """Prueba la configuración de Gmail SMTP"""
    
    # Cargar variables de entorno
    load_dotenv()
    
    print("🔧 PROBANDO CONFIGURACIÓN DE GMAIL SMTP")
    print("=" * 45)
    
    # Verificar configuraciones
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    
    print(f"📧 Email Usuario: {email_user}")
    print(f"🔒 Password configurado: {'✅ Sí' if email_password else '❌ No'}")
    print(f"🌐 Servidor SMTP: {smtp_server}")
    print(f"🔌 Puerto SMTP: {smtp_port}")
    
    if not email_user or not email_password:
        print("\n❌ ERROR: Configuración incompleta")
        print("Por favor configura EMAIL_USER y EMAIL_PASSWORD en el archivo .env")
        print("Revisa el archivo GMAIL_SMTP_SETUP.md para instrucciones detalladas")
        return False
    
    print(f"\n🧪 Enviando email de prueba a {email_user}...")
    
    # Probar configuración
    try:
        success = test_email_configuration()
        
        if success:
            print("✅ EMAIL DE PRUEBA ENVIADO EXITOSAMENTE!")
            print(f"📬 Revisa tu bandeja de entrada en {email_user}")
            print("📁 Si no lo ves, revisa la carpeta de spam")
        else:
            print("❌ ERROR: No se pudo enviar el email de prueba")
            
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        return False
    
    # Probar email de recuperación
    print(f"\n🔑 Probando email de recuperación de contraseña...")
    
    try:
        test_token = "test_token_123456789"
        success = send_reset_email(
            email=email_user,
            token=test_token,
            nombre="Usuario de Prueba"
        )
        
        if success:
            print("✅ EMAIL DE RECUPERACIÓN ENVIADO EXITOSAMENTE!")
        else:
            print("❌ ERROR: No se pudo enviar el email de recuperación")
            
    except Exception as e:
        print(f"❌ ERROR EN EMAIL DE RECUPERACIÓN: {e}")
    
    print("\n🎉 PRUEBA COMPLETADA")
    print("Revisa tu bandeja de entrada para confirmar que llegaron los emails")
    
    return True

if __name__ == "__main__":
    main()