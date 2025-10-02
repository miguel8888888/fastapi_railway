"""
Servicio de email usando webhook gratuito - Sin necesidad de registros externos
Usa servicios gratuitos como EmailJS o Formspree
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

def send_email_via_webhook(to_email: str, subject: str, message: str) -> bool:
    """
    Envía email usando un webhook gratuito (sin registro)
    Opción 1: Usar EmailJS (solo requiere configuración frontend)
    Opción 2: Usar servicio webhook gratuito
    """
    
    # Configuración del webhook
    webhook_url = os.getenv("EMAIL_WEBHOOK_URL")
    
    if not webhook_url:
        logger.error("EMAIL_WEBHOOK_URL no configurado")
        return False
    
    try:
        # Datos para el webhook
        payload = {
            "to": to_email,
            "subject": subject,
            "message": message,
            "from": os.getenv("FROM_EMAIL", "noreply@numismatica.com")
        }
        
        # Enviar via webhook
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"Email enviado via webhook a {to_email}")
            return True
        else:
            logger.error(f"Error webhook: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error enviando email via webhook: {e}")
        return False

def send_email_via_formsubmit(to_email: str, subject: str, message: str) -> bool:
    """
    Usa FormSubmit.co - Servicio gratuito sin registro
    """
    
    try:
        # FormSubmit.co permite enviar emails gratis
        url = "https://formsubmit.co/ajax/miguelsgap@gmail.com"
        
        payload = {
            "name": "Sistema Numismática",
            "email": to_email,
            "subject": subject,
            "message": message,
            "_captcha": "false",
            "_template": "table"
        }
        
        response = requests.post(url, data=payload, timeout=30)
        
        if response.status_code == 200:
            logger.info(f"Email enviado via FormSubmit a {to_email}")
            return True
        else:
            logger.error(f"Error FormSubmit: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error FormSubmit: {e}")
        return False