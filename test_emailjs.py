"""
Script de prueba para EmailJS - Ejecutar después de configurar las variables
"""

import os
from app.utils.email_emailjs import test_emailjs_config

print("PRUEBA DE EMAILJS EN LOCAL")
print("=" * 30)

# Verificar configuración
service_id = os.getenv("EMAILJS_SERVICE_ID")
template_id = os.getenv("EMAILJS_TEMPLATE_ID") 
public_key = os.getenv("EMAILJS_PUBLIC_KEY")

print(f"Service ID: {service_id or 'NO CONFIGURADO'}")
print(f"Template ID: {template_id or 'NO CONFIGURADO'}")
print(f"Public Key: {public_key or 'NO CONFIGURADO'}")

if not all([service_id, template_id, public_key]):
    print("\n❌ ERROR: Variables EmailJS no configuradas")
    print("\nConfigura en tu .env:")
    print("EMAILJS_SERVICE_ID=service_xxxxxxx")
    print("EMAILJS_TEMPLATE_ID=template_xxxxxxx")
    print("EMAILJS_PUBLIC_KEY=xxxxxxxxxxxxxxx")
    exit(1)

print(f"\n✅ Variables configuradas correctamente")
print(f"Enviando email de prueba...")

# Probar EmailJS
success = test_emailjs_config()

if success:
    print("✅ EMAIL ENVIADO EXITOSAMENTE!")
    print("Revisa tu Gmail: miguelsgap@gmail.com")
    print("¡EmailJS está funcionando perfectamente!")
else:
    print("❌ Error enviando email")
    print("Verifica tu configuración EmailJS")