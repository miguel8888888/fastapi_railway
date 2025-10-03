"""
Servicio de email usando Resend.com - Muy fácil para backend
Resend es específicamente diseñado para envío desde servidores
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

def send_email_resend(to_email: str, subject: str, html_content: str, from_name: str = "Sistema Numismática") -> bool:
    """
    Envía email usando Resend.com - Perfecto para backend
    3000 emails/mes gratis, muy fácil configuración
    """
    
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "miguelsgap@gmail.com")
    
    if not api_key:
        logger.error("RESEND_API_KEY no configurada")
        return False
    
    try:
        # URL de Resend API
        url = "https://api.resend.com/emails"
        
        # Headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Datos del email
        data = {
            "from": f"{from_name} <{from_email}>",
            "to": [to_email],
            "subject": subject,
            "html": html_content
        }
        
        # Enviar request
        response = requests.post(
            url,
            json=data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"Email enviado via Resend a {to_email}")
            return True
        else:
            logger.error(f"Error Resend: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error enviando email via Resend: {e}")
        return False


def test_resend_config() -> bool:
    """
    Prueba la configuración de Resend
    """
    
    test_email = os.getenv("FROM_EMAIL", "miguelsgap@gmail.com")
    
    return send_email_resend(
        to_email=test_email,
        subject="Prueba Resend - Sistema Numismática",
        html_content="""
        <h2>Prueba de Resend</h2>
        <p>Este email confirma que Resend está funcionando correctamente.</p>
        <p><strong>Ventajas de Resend:</strong></p>
        <ul>
            <li>✅ 3000 emails/mes gratis</li>
            <li>✅ Perfecto para backend</li>
            <li>✅ Muy fácil configuración</li>
            <li>✅ Funciona en Render</li>
        </ul>
        """,
        from_name="Sistema Numismática"
    )