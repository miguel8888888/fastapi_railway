"""
Servicio de email usando EmailJS - Envío directo al usuario
EmailJS permite enviar emails directamente sin backend SMTP
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

def send_email_emailjs(to_email: str, to_name: str, subject: str, message: str, reset_url: str = None) -> dict:
    """
    Envía email usando EmailJS - Servicio gratuito con envío directo
    Límite: 200 emails/mes gratis
    """
    
    # Configuración EmailJS
    service_id = os.getenv("EMAILJS_SERVICE_ID", "service_xxxxxxx")
    template_id = os.getenv("EMAILJS_TEMPLATE_ID", "template_xxxxxxx") 
    public_key = os.getenv("EMAILJS_PUBLIC_KEY", "xxxxxxxxxxxxxxx")
    private_key = os.getenv("EMAILJS_PRIVATE_KEY", "xxxxxxxxxxxxxxx")  # Clave privada para backend
    
    if not all([service_id, template_id, public_key]):
        logger.error("Credenciales EmailJS no configuradas")
        return {"success": False, "error": "Credenciales EmailJS no configuradas"}
    
    # Usar clave privada si está disponible, sino public key
    auth_key = private_key if private_key else public_key
    
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
            "from_email": "miguelsgap@gmail.com",
            "reply_to": "miguelsgap@gmail.com"
        }
        
        # Si hay URL de reset, agregarla
        if reset_url:
            template_params["reset_url"] = reset_url
            template_params["reset_link"] = f'<a href="{reset_url}" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Restablecer Contraseña</a>'
            template_params["reset_button"] = f'{reset_url}'
        
        # Payload para EmailJS 
        payload = {
            "service_id": service_id,
            "template_id": template_id,
            "user_id": public_key,
            "template_params": template_params
        }
        
        # Si tenemos clave privada, agregarla para llamadas de backend
        if private_key:
            payload["accessToken"] = private_key
        
        # Headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # Log para debug
        logger.info(f"Enviando email a {to_email} con URL: {reset_url if reset_url else 'sin URL'}")
        
        # Enviar request
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"Email enviado via EmailJS a {to_email}")
            return {"success": True, "message": "Email enviado correctamente"}
        else:
            error_msg = f"Error EmailJS: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
            
    except Exception as e:
        error_msg = f"Error enviando email via EmailJS: {e}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}


def test_emailjs_config() -> dict:
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