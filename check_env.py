"""
Script simple para verificar la configuración de variables de entorno
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("🔧 Verificación de Variables de Entorno")
print("="*50)

# Variables importantes para email
variables = {
    "FRONTEND_URL": os.getenv("FRONTEND_URL"),
    "EMAILJS_SERVICE_ID": os.getenv("EMAILJS_SERVICE_ID"),
    "EMAILJS_TEMPLATE_ID": os.getenv("EMAILJS_TEMPLATE_ID"),
    "EMAILJS_PUBLIC_KEY": os.getenv("EMAILJS_PUBLIC_KEY"),
    "EMAILJS_PRIVATE_KEY": os.getenv("EMAILJS_PRIVATE_KEY"),
    "EMAIL_USER": os.getenv("EMAIL_USER"),
}

for var_name, var_value in variables.items():
    if var_value:
        if "KEY" in var_name or "PASSWORD" in var_name:
            # Mostrar solo los primeros y últimos caracteres por seguridad
            if len(var_value) > 8:
                masked_value = f"{var_value[:4]}...{var_value[-4:]}"
            else:
                masked_value = "***"
            print(f"✅ {var_name}: {masked_value}")
        else:
            print(f"✅ {var_name}: {var_value}")
    else:
        print(f"❌ {var_name}: No configurada")

print("\n" + "="*50)

# Simulación de URL de reset
token = "test_token_123456789"
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:4200")
reset_url = f"{frontend_url}/auth/reset-password?token={token}"

print(f"🔗 URL de reset que se generaría:")
print(f"   {reset_url}")

if "numismatica.onrender.com" in reset_url:
    print("✅ La URL apunta correctamente a Render!")
elif "localhost" in reset_url:
    print("⚠️  La URL todavía apunta a localhost")
else:
    print(f"⚠️  La URL tiene un dominio inesperado: {reset_url}")

print("\n" + "="*50)
print("✅ Verificación completada")