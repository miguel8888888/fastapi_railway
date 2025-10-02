import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

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
    
    # Template del email
    subject = "Recuperación de Contraseña - Sistema Numismático"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Recuperación de Contraseña</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
            <h2 style="color: #333; text-align: center;">Recuperación de Contraseña</h2>
            
            <p>Hola <strong>{nombre}</strong>,</p>
            
            <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en el Sistema Numismático.</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #007bff; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 4px; display: inline-block;">
                    Restablecer Contraseña
                </a>
            </div>
            
            <p>Si no puedes hacer clic en el botón, copia y pega este enlace en tu navegador:</p>
            <p style="background-color: #e9ecef; padding: 10px; border-radius: 4px; word-break: break-all;">
                {reset_url}
            </p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6;">
                <p style="color: #6c757d; font-size: 14px;">
                    <strong>Importante:</strong>
                    <br>• Este enlace expira en 24 horas
                    <br>• Si no solicitaste este cambio, puedes ignorar este email
                    <br>• Por tu seguridad, no compartas este enlace con nadie
                </p>
            </div>
            
            <p style="color: #6c757d; font-size: 12px; text-align: center; margin-top: 20px;">
                Sistema Numismático - Gestión de Colecciones
            </p>
        </div>
    </body>
    </html>
    """
    
    # Implementación con Gmail SMTP
    try:
        return send_email_smtp(
            to_email=email,
            subject=subject,
            html_content=html_content
        )
    except Exception as e:
        logger.error(f"Error enviando email de recuperación a {email}: {e}")
        # En desarrollo, mostrar en consola como fallback
        print(f"""
        ==================== EMAIL DE RECUPERACIÓN ====================
        Para: {email}
        Asunto: {subject}
        
        Token: {token}
        URL de reset: {reset_url}
        
        Error enviando email: {e}
        ===============================================================
        """)
        return False

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

def send_email_smtp(to_email: str, subject: str, html_content: str) -> bool:
    """
    Envía email usando Gmail SMTP
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
    
    return send_email_smtp(
        to_email=email_user,  # Enviar a uno mismo como prueba
        subject=test_subject,
        html_content=test_content
    )