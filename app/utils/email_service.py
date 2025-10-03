import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging
import requests
import re

# Configurar logging para emails
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_reset_email(email: str, token: str, nombre: str = "Usuario"):
    """
    Envía email de recuperación de contraseña.
    
    En producción, deberías usar un servicio como:
    - SendGrid
    - AWS SES  
    - Mailgun
    - SMTP
    """
    
    # URL del frontend donde el usuario resetea la contraseña
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:4200")
    reset_url = f"{frontend_url}/auth/reset-password?token={token}"
    
    # Log para debug de la URL
    logger.info(f"Enviando email de recuperación a {email}")
    logger.info(f"Frontend URL configurada: {frontend_url}")
    logger.info(f"URL completa de reset: {reset_url}")
    
    # Template del email
    subject = "Recuperación de Contraseña - Sistema Numismático"
    
    # Template HTML simple para EmailJS (sin CSS en <head>)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
        <div style="background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #333; text-align: center; margin-bottom: 30px;">🔐 Recuperación de Contraseña</h2>
            
            <p style="font-size: 16px; color: #333;">Hola <strong>{nombre}</strong>,</p>
            
            <p style="color: #666; line-height: 1.5;">Recibimos una solicitud para restablecer la contraseña de tu cuenta en el Sistema Numismático.</p>
            
            <div style="text-align: center; margin: 40px 0;">
                <a href="{reset_url}" 
                   style="background-color: #007bff; color: white; padding: 15px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block; 
                          font-weight: bold; font-size: 16px; border: none;">
                    🔑 Restablecer Contraseña
                </a>
            </div>
            
            <p style="color: #333; font-weight: bold; margin-top: 30px;">Si no puedes hacer clic en el botón, copia este enlace:</p>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 4px; border: 1px solid #dee2e6; margin: 15px 0;">
                <p style="color: #007bff; word-break: break-all; margin: 0; font-family: monospace;">
                    {reset_url}
                </p>
            </div>
            
            <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #dee2e6;">
                <p style="color: #666; font-size: 14px; line-height: 1.6;">
                    <strong style="color: #dc3545;">⚠️ Importante:</strong><br>
                    • Este enlace expira en 24 horas<br>
                    • Si no solicitaste este cambio, ignora este email<br>
                    • Por tu seguridad, no compartas este enlace
                </p>
            </div>
            
            <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                🪙 Sistema Numismático - Gestión de Colecciones
            </p>
        </div>
    </body>
    </html>
    """
    
    # Template de texto plano como fallback
    plain_text = f"""
    Hola {nombre},
    
    Recibimos una solicitud para restablecer tu contraseña.
    
    Haz clic en este enlace para restablecer tu contraseña:
    {reset_url}
    
    Este enlace expira en 24 horas.
    
    Si no solicitaste este cambio, puedes ignorar este email.
    
    Sistema Numismático
    """
    
    # Estrategia de envío: SMTP (temporal para debug) -> EmailJS -> FormSubmit -> SendGrid
    success = False
    
    # 1. Usar SMTP directamente para evitar problemas de EmailJS
    logger.info("Usando SMTP directamente para evitar problemas de formato...")
    try:
        success = send_email_smtp(
            to_email=email,
            subject=subject,
            html_content=html_content
        )
        if success:
            logger.info("✅ Email enviado exitosamente via SMTP")
        else:
            logger.warning("❌ SMTP falló, intentando EmailJS...")
    except Exception as e:
        logger.error(f"Error con SMTP: {e}")
        success = False
    
    # 2. Si SMTP falla, intentar EmailJS
    if not success and os.getenv("EMAILJS_SERVICE_ID"):
        logger.info("Intentando EmailJS como alternativa...")
        success = send_email_emailjs(
            to_email=email,
            subject=subject,
            html_content=plain_text,  # Enviar solo texto plano a EmailJS
            nombre=nombre
        )
    
    # 2. Si no funciona, usar FormSubmit como fallback (te envía a ti)
    if not success:
        logger.info("EmailJS falló, intentando FormSubmit...")
        success = send_email_formsubmit(
            to_email=email,
            subject=subject,
            html_content=html_content
        )
    
    # 3. Si no funciona, intentar SendGrid (si está configurado)
    if not success and os.getenv("SENDGRID_API_KEY"):
        logger.info("Intentando SendGrid...")
        success = send_email_sendgrid(
            to_email=email,
            subject=subject,
            html_content=html_content
        )
    
    # 4. Último recurso: SMTP (puede fallar en Render)
    if not success:
        logger.info("Intentando SMTP como último recurso...")
        try:
            success = send_email_smtp(
                to_email=email,
                subject=subject,
                html_content=html_content
            )
        except Exception as e:
            logger.error(f"SMTP también falló: {e}")
            success = False
    
    if not success:
        logger.error(f"Error enviando email de recuperación a {email}")
        # En desarrollo, mostrar en consola como fallback
        print(f"""
        ==================== EMAIL DE RECUPERACIÓN ====================
        Para: {email}
        Asunto: {subject}
        
        Token: {token}
        URL de reset: {reset_url}
        
        Todos los métodos de email fallaron
        ===============================================================
        """)
    
    return success

def send_welcome_email(email: str, nombre: str, password: str):
    """
    Envía email de bienvenida con credenciales temporales
    """
    
    subject = "Bienvenido al Sistema Numismático"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
            <h2 style="color: #333; text-align: center;">¡Bienvenido al Sistema Numismático!</h2>
            
            <p>Hola <strong>{nombre}</strong>,</p>
            
            <p>Tu cuenta ha sido creada exitosamente. Aquí están tus credenciales:</p>
            
            <div style="background-color: #e9ecef; padding: 15px; border-radius: 4px; margin: 20px 0;">
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Contraseña temporal:</strong> {password}</p>
            </div>
            
            <p style="color: #dc3545;">
                <strong>⚠️ Importante:</strong> Por tu seguridad, te recomendamos cambiar esta contraseña 
                temporal en tu primer inicio de sesión.
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{os.getenv('FRONTEND_URL', 'http://localhost:4200')}/auth/login" 
                   style="background-color: #28a745; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 4px; display: inline-block;">
                    Iniciar Sesión
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Implementación con Gmail SMTP para bienvenida
    try:
        return send_email_smtp(
            to_email=email,
            subject=subject,
            html_content=html_content
        )
    except Exception as e:
        logger.error(f"Error enviando email de bienvenida a {email}: {e}")
        # En desarrollo, mostrar en consola como fallback
        print(f"""
        ==================== EMAIL DE BIENVENIDA ====================
        Para: {email}
        Asunto: {subject}
        
        Credenciales:
        Email: {email}
        Contraseña temporal: {password}
        
        Error enviando email: {e}
        ===============================================================
        """)
        return False

def send_email_sendgrid(to_email: str, subject: str, html_content: str) -> bool:
    """
    Envía email usando SendGrid API (recomendado para producción)
    """
    
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "miguelsgap@gmail.com")
    
    if not sendgrid_api_key:
        logger.error("SENDGRID_API_KEY no configurada")
        return False
    
    try:
        # Preparar datos para SendGrid API
        data = {
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "subject": subject
                }
            ],
            "from": {"email": from_email, "name": "Sistema Numismática"},
            "content": [
                {
                    "type": "text/html",
                    "value": html_content
                }
            ]
        }
        
        # Enviar via SendGrid API
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {sendgrid_api_key}",
                "Content-Type": "application/json"
            },
            json=data
        )
        
        if response.status_code == 202:
            logger.info(f"Email enviado exitosamente via SendGrid a {to_email}")
            return True
        else:
            logger.error(f"Error SendGrid: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error general enviando email via SendGrid: {e}")
        return False

def send_email_formsubmit(to_email: str, subject: str, html_content: str) -> bool:
    """
    Envía email usando FormSubmit.co - Servicio gratuito sin registro
    Límite: 500 emails/mes por dominio
    """
    
    try:
        # Convertir HTML a texto plano para FormSubmit
        plain_text = re.sub('<[^<]+?>', '', html_content)
        plain_text = plain_text.replace('&nbsp;', ' ').strip()
        
        # FormSubmit.co endpoint (usa tu email como destino)
        from_email = os.getenv("FROM_EMAIL", "miguelsgap@gmail.com")
        url = f"https://formsubmit.co/ajax/{from_email}"
        
        # Datos del formulario
        form_data = {
            "_subject": subject,
            "_email": {
                "from": "Sistema Numismática",
                "reply": to_email
            },
            "_next": "https://thankyou.com",
            "_captcha": "false",
            "_template": "box",
            "email_destino": to_email,
            "mensaje": plain_text,
            "tipo": "Recuperacion de Contraseña"
        }
        
        # Headers necesarios
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Enviar request
        response = requests.post(
            url,
            json=form_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"Email enviado via FormSubmit a {to_email}")
            return True
        else:
            logger.error(f"Error FormSubmit: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error enviando email via FormSubmit: {e}")
        return False

def send_email_emailjs(to_email: str, subject: str, html_content: str, nombre: str = "Usuario") -> bool:
    """
    Envía email usando EmailJS - Envío directo al usuario final
    """
    
    try:
        # Importar la función EmailJS
        from app.utils.email_emailjs import send_email_emailjs as emailjs_send
        
        # Convertir HTML a texto para el mensaje
        plain_text = re.sub('<[^<]+?>', '', html_content)
        plain_text = plain_text.replace('&nbsp;', ' ').strip()
        
        # Extraer URL de reset si existe
        reset_url = None
        url_match = re.search(r'http[s]?://[^\s<>"]+reset-password[^\s<>"]*', html_content)
        if url_match:
            reset_url = url_match.group()
        
        # Enviar via EmailJS
        result = emailjs_send(
            to_email=to_email,
            to_name=nombre,
            subject=subject,
            message=plain_text,
            reset_url=reset_url
        )
        
        # La nueva función devuelve dict, extraer success
        if isinstance(result, dict):
            return result.get('success', False)
        else:
            return bool(result)
        
    except Exception as e:
        logger.error(f"Error enviando email via EmailJS: {e}")
        return False

def send_email_smtp(to_email: str, subject: str, html_content: str) -> bool:
    """
    Envía email usando Gmail SMTP (puede no funcionar en algunas plataformas)
    """
    
    # Configuraciones SMTP de Gmail
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    from_email = os.getenv("FROM_EMAIL", email_user)
    
    if not email_user or not email_password:
        logger.error("Credenciales de email no configuradas en variables de entorno")
        return False
    
    try:
        # Crear mensaje
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = to_email
        
        # Agregar contenido HTML
        html_part = MIMEText(html_content, "html", "utf-8")
        message.attach(html_part)
        
        # Conectar y enviar
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Habilitar seguridad TLS
            server.login(email_user, email_password)
            server.sendmail(from_email, to_email, message.as_string())
        
        logger.info(f"Email enviado exitosamente a {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error("Error de autenticación SMTP - Verifica las credenciales de Gmail")
        return False
    except smtplib.SMTPRecipientsRefused:
        logger.error(f"Email rechazado: {to_email}")
        return False
    except Exception as e:
        logger.error(f"Error general enviando email: {e}")
        return False

def test_email_configuration() -> bool:
    """
    Prueba la configuración de email enviando un email de prueba
    """
    
    email_user = os.getenv("EMAIL_USER")
    if not email_user:
        logger.error("EMAIL_USER no configurado")
        return False
    
    test_subject = "Prueba de Configuración SMTP - Sistema Numismática"
    test_content = """
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
            <h2 style="color: #28a745; text-align: center;">✅ Configuración SMTP Exitosa</h2>
            <p>Este es un email de prueba para verificar que la configuración de Gmail SMTP está funcionando correctamente.</p>
            <p><strong>Sistema:</strong> Sistema Numismática</p>
            <p><strong>Fecha:</strong> {}</p>
        </div>
    </body>
    </html>
    """.format(os.popen('date /t').read().strip() if os.name == 'nt' else os.popen('date').read().strip())
    
    # Estrategia de test: SendGrid -> FormSubmit -> SMTP
    success = False
    
    # 1. Intentar SendGrid si está configurado
    if os.getenv("SENDGRID_API_KEY"):
        success = send_email_sendgrid(
            to_email=email_user,
            subject=test_subject,
            html_content=test_content
        )
    
    # 2. Si no funciona, usar FormSubmit (gratuito)
    if not success:
        logger.info("Usando FormSubmit para test...")
        success = send_email_formsubmit(
            to_email=email_user,
            subject=test_subject,
            html_content=test_content
        )
    
    # 3. Último recurso: SMTP
    if not success:
        logger.info("Intentando SMTP como último recurso...")
        success = send_email_smtp(
            to_email=email_user,
            subject=test_subject,
            html_content=test_content
        )
    
    return success