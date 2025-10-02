"""
Servicio de email usando EmailJS - Envío directo al usuario
EmailJS permite enviar emails directamente sin backend SMTP
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

def send_email_emailjs(to_email: str, to_name: str, subject: str, message: str, reset_url: str = None) -> bool:
    """
    Envía email usando EmailJS - Servicio gratuito con envío directo
    Límite: 200 emails/mes gratis
    """
    
    # Configuración EmailJS (obtendrás estos valores al registrarte)
    service_id = os.getenv("EMAILJS_SERVICE_ID", "service_xxxxxxx")
    template_id = os.getenv("EMAILJS_TEMPLATE_ID", "template_xxxxxxx") 
    public_key = os.getenv("EMAILJS_PUBLIC_KEY", "xxxxxxxxxxxxxxx")
    
    if not all([service_id, template_id, public_key]):
        logger.error("Credenciales EmailJS no configuradas")
        return False
    
    try:
        # Endpoint de EmailJS
        url = "https://api.emailjs.com/api/v1.0/email/send"
        
        # Datos del template
        template_params = {
            "to_email": to_email,
            "to_name": to_name,
            "subject": subject,
            "message": message,
            "from_name": "Sistema Numismática",
            "from_email": "miguelsgap@gmail.com"
        }
        
        # Si hay URL de reset, agregarla
        if reset_url:
            template_params["reset_url"] = reset_url
            template_params["reset_link"] = f'<a href="{reset_url}">Restablecer Contraseña</a>'
        
        # Payload para EmailJS
        payload = {
            "service_id": service_id,
            "template_id": template_id,
            "user_id": public_key,
            "template_params": template_params
        }
        
        # Headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # Enviar request
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"Email enviado via EmailJS a {to_email}")
            return True
        else:
            logger.error(f"Error EmailJS: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error enviando email via EmailJS: {e}")
        return False


def test_emailjs_config() -> bool:
    """
    Prueba la configuración EmailJS enviando un email de prueba
    """
    
    test_email = os.getenv("FROM_EMAIL", "miguelsgap@gmail.com")
    
    return send_email_emailjs(
        to_email=test_email,
        to_name="Administrador",
        subject="Prueba EmailJS - Sistema Numismática",
        message="Este es un email de prueba para verificar que EmailJS está funcionando correctamente."
    )