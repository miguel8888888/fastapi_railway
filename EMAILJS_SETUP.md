# Configuración EmailJS - Paso a Paso

## 🚀 EmailJS Setup (5 minutos)

EmailJS permite enviar emails **directamente al usuario final** de forma gratuita.

### ✅ Ventajas:
- **200 emails/mes gratis**
- **Envío directo** al usuario (no a ti)
- **Funciona en Render**
- **Emails inmediatos**
- **Fácil configuración**

## 📋 Pasos de Configuración:

### 1. Crear Cuenta EmailJS
1. Ve a **https://www.emailjs.com**
2. Clic en **"Sign Up"**
3. Completa el registro
4. **Verifica tu email**

### 2. Configurar Servicio Gmail
1. En el dashboard, clic **"Add New Service"**
2. Selecciona **"Gmail"**
3. Clic **"Connect Account"**
4. **Autoriza con `miguelsgap@gmail.com`**
5. **Copia el Service ID** (ej: `service_abc123`)

### 3. Crear Template de Email
1. Ve a **"Email Templates"**
2. Clic **"Create New Template"**
3. **Configura el template:**

```html
Asunto: {{subject}}

Hola {{to_name}},

{{message}}

{{#reset_url}}
Haz clic aquí para restablecer tu contraseña:
{{reset_url}}
{{/reset_url}}

Saludos,
{{from_name}}
```

4. **Guarda y copia el Template ID** (ej: `template_xyz789`)

### 4. Obtener Public Key
1. Ve a **"Account"** → **"General"**
2. **Copia el Public Key** (ej: `abc123defg456`)

### 5. Configurar Variables de Entorno

Agrega estas variables en tu `.env` local:

```env
EMAILJS_SERVICE_ID=service_abc123
EMAILJS_TEMPLATE_ID=template_xyz789
EMAILJS_PUBLIC_KEY=abc123defg456
```

### 6. Probar Localmente

```bash
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar servidor
python -m uvicorn app.main:app --reload --port 8000
```

### 7. Probar EmailJS

```bash
# Login como admin y probar EmailJS
POST http://localhost:8000/auth/test-emailjs/
```

## 🔧 Configuración en Render

Una vez que funcione localmente:

1. **Ve a tu panel de Render**
2. **Selecciona tu servicio**
3. **Environment Variables**
4. **Agrega:**
   - `EMAILJS_SERVICE_ID=service_abc123`
   - `EMAILJS_TEMPLATE_ID=template_xyz789`
   - `EMAILJS_PUBLIC_KEY=abc123defg456`

## ✅ Resultado Final

Con EmailJS configurado:
- ✅ **Usuarios reciben emails directamente**
- ✅ **200 emails/mes gratis**
- ✅ **Funciona perfectamente en Render**
- ✅ **Envío inmediato**

## 🎯 Estrategia de Envío Final:

1. **EmailJS** (directo al usuario)
2. **FormSubmit** (fallback, envía a ti)
3. **SMTP** (último recurso)

¡La mejor de ambos mundos! 🚀