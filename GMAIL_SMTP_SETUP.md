# 📧 CONFIGURACIÓN DE GMAIL SMTP - Sistema Numismática

## 🔧 Pasos para Configurar Gmail SMTP

### 1. Habilitar Verificación en 2 Pasos
1. Ve a tu **Cuenta de Google**: https://myaccount.google.com/
2. En el menú izquierdo, selecciona **Seguridad**
3. En "Iniciar sesión en Google", selecciona **Verificación en 2 pasos**
4. Sigue los pasos para habilitar la verificación en 2 pasos

### 2. Generar Contraseña de Aplicación
1. Una vez habilitada la verificación en 2 pasos, regresa a **Seguridad**
2. En "Iniciar sesión en Google", selecciona **Contraseñas de aplicaciones**
3. Selecciona la aplicación: **Correo**
4. Selecciona el dispositivo: **Otro (nombre personalizado)**
5. Escribe: **Sistema Numismática**
6. Haz clic en **Generar**
7. **Copia la contraseña de 16 caracteres** que aparece

### 3. Actualizar Variables de Entorno

En tu archivo `.env`, actualiza:

```env
# Configuración de Gmail SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=miguelsgap@gmail.com
EMAIL_PASSWORD=AQUI_VA_TU_CONTRASEÑA_DE_APLICACION_DE_16_CARACTERES
FROM_EMAIL=miguelsgap@gmail.com
TOKEN_EXPIRATION=3600
```

**⚠️ IMPORTANTE:**
- Usa la **contraseña de aplicación** (16 caracteres), NO tu contraseña normal de Gmail
- Esta contraseña se ve algo así: `abcd efgh ijkl mnop`
- NO incluyas espacios en el archivo .env

### 4. Configurar en Render (Producción)

En el dashboard de Render, agrega estas variables de entorno:

- `SMTP_SERVER` = `smtp.gmail.com`
- `SMTP_PORT` = `587`
- `EMAIL_USER` = `miguelsgap@gmail.com`
- `EMAIL_PASSWORD` = `tu_contraseña_de_aplicacion_sin_espacios`
- `FROM_EMAIL` = `miguelsgap@gmail.com`
- `TOKEN_EXPIRATION` = `3600`

## 🧪 Probar la Configuración

### Localmente:
1. Actualiza tu archivo `.env` con la contraseña de aplicación
2. Inicia el servidor: `uvicorn app.main:app --reload`
3. Ve a: http://127.0.0.1:8000/docs
4. Usa el endpoint `/auth/test-email/` (necesitas ser admin)

### En Render:
1. Configura las variables de entorno en Render
2. Haz deployment del código
3. Usa el endpoint de prueba desde la URL de producción

## 🔍 Template del Email de Recuperación

El sistema enviará emails con este formato:

**Asunto:** "Recupera tu contraseña - Sistema Numismática"

**Contenido:**
- Saludo personalizado con el nombre del usuario
- Botón para restablecer contraseña
- URL directa como alternativa
- Información de seguridad (expira en 1 hora)
- Diseño responsive y profesional

## 🛠️ Endpoints Disponibles

### Solicitar Recuperación
```
POST /auth/forgot-password/
{
  "email": "usuario@email.com"
}
```

### Verificar Token
```
GET /auth/verify-token/{token}
```

### Resetear Contraseña
```
POST /auth/reset-password/
{
  "token": "token_de_recuperacion",
  "new_password": "nueva_contraseña"
}
```

### Probar Email (Solo Admin)
```
POST /auth/test-email/
```

## 🔒 Seguridad

- Los tokens expiran en 1 hora (configurable)
- Se registra IP y User Agent para auditoría
- Los tokens usados se marcan como utilizados
- Sistema de rate limiting para prevenir spam
- Limpieza automática de tokens expirados

## ❗ Solución de Problemas

### Error de Autenticación:
- Verifica que uses la contraseña de aplicación, no la contraseña normal
- Asegúrate de tener habilitada la verificación en 2 pasos
- Revisa que no haya espacios en la contraseña

### Email no llega:
- Revisa la carpeta de spam
- Verifica que el email destino sea válido
- Revisa los logs del servidor para errores SMTP

### Error de conexión:
- Verifica la conexión a internet
- Asegúrate que el puerto 587 no esté bloqueado
- Confirma las configuraciones SMTP_SERVER y SMTP_PORT