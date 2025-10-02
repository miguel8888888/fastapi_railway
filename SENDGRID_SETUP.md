# Configuración SendGrid para Render

## Problema
Render bloquea conexiones SMTP salientes (puerto 587), por lo que Gmail SMTP no funciona en producción.

## Solución: SendGrid
SendGrid es un servicio de email que funciona perfectamente con Render usando API REST.

## Pasos para Configurar SendGrid:

### 1. Crear Cuenta SendGrid (Gratuita)
1. Ve a [sendgrid.com](https://sendgrid.com)
2. Crea una cuenta gratuita (100 emails/día gratis)
3. Verifica tu email

### 2. Obtener API Key
1. Ve a **Settings** → **API Keys**
2. Clic en **Create API Key**
3. Nombre: "FastAPI Railway"
4. Permisos: **Restricted Access**
5. Solo marca: **Mail Send** → **Full Access**
6. **Create & View**
7. **COPIA LA API KEY** (solo se muestra una vez)

### 3. Verificar Sender Identity
1. Ve a **Settings** → **Sender Authentication**
2. **Authenticate Your Domain** (recomendado) o **Single Sender Verification**
3. Si usas Single Sender: verifica `miguelsgap@gmail.com`

### 4. Configurar en Render
En tu panel de Render, agrega esta variable:
```
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxx
```

### 5. Desplegar Cambios
```bash
git add .
git commit -m "feat: Add SendGrid support for email in production"
git push
```

Render redesplegará automáticamente con la nueva configuración.

## Verificación
Una vez configurado, el sistema:
1. Intentará SendGrid primero
2. Si falla, intentará SMTP como fallback
3. Los logs mostrarán qué método funcionó

## Ventajas de SendGrid
- ✅ Funciona en Render
- ✅ 100 emails/día gratis
- ✅ Mejor deliverability
- ✅ Estadísticas de emails
- ✅ No requiere contraseñas de aplicación

## Notas Importantes
- La API key debe empezar con `SG.`
- FROM_EMAIL debe estar verificado en SendGrid
- El plan gratuito es suficiente para pruebas y uso pequeño