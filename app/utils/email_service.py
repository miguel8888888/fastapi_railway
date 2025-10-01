import os
from typing import Optional

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
    
    # TODO: Implementar envío real del email
    # Ejemplo con SendGrid:
    # import sendgrid
    # from sendgrid.helpers.mail import Mail
    # 
    # sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    # from_email = os.environ.get('FROM_EMAIL', 'noreply@tudominio.com')
    # 
    # message = Mail(
    #     from_email=from_email,
    #     to_emails=email,
    #     subject=subject,
    #     html_content=html_content
    # )
    # 
    # try:
    #     response = sg.send(message)
    #     return True
    # except Exception as e:
    #     print(f"Error sending email: {e}")
    #     return False
    
    # Por ahora, solo imprimimos en consola para desarrollo
    print(f"""
    ==================== EMAIL DE RECUPERACIÓN ====================
    Para: {email}
    Asunto: {subject}
    
    Token: {token}
    URL de reset: {reset_url}
    
    En producción, este email se enviaría automáticamente.
    ===============================================================
    """)
    
    return True

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
    
    print(f"""
    ==================== EMAIL DE BIENVENIDA ====================
    Para: {email}
    Asunto: {subject}
    
    Credenciales:
    Email: {email}
    Contraseña temporal: {password}
    ===============================================================
    """)
    
    return True