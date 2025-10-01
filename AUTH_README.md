# 🔐 Sistema de Autenticación - FastAPI

Este proyecto implementa un sistema de autenticación completo según las especificaciones del documento `DATABASE_SCHEMA.md`.

## 🚀 Características Implementadas

### ✅ Endpoints de Autenticación
- `POST /auth/login/` - Login de usuario
- `POST /auth/logout/` - Cerrar sesión  
- `POST /auth/forgot-password/` - Solicitar recuperación
- `POST /auth/reset-password/` - Resetear contraseña con token
- `GET /auth/verify-token/{token}` - Verificar token de recuperación
- `GET /auth/me/` - Información del usuario actual

### ✅ Gestión de Usuarios (Admin)
- `GET /auth/users/` - Listar usuarios
- `POST /auth/users/` - Crear usuario (solo super_admin)
- `GET /auth/users/{id}` - Obtener usuario por ID
- `PUT /auth/users/{id}` - Actualizar usuario
- `DELETE /auth/users/{id}` - Eliminar usuario (solo super_admin)
- `POST /auth/users/{id}/reset-password` - Resetear contraseña

### ✅ Características de Seguridad
- **Hashing bcrypt**: Salt rounds = 12
- **JWT seguro**: Tokens con expiración de 30 minutos
- **Rate limiting**: Máximo 5 intentos por IP/hora
- **Tokens de recuperación**: Expiran en 24 horas, un solo uso
- **Validación de contraseñas**: Mínimo 8 caracteres, mayúsculas, minúsculas y números
- **Protección contra ataques**: Bloqueo temporal tras 5 intentos fallidos

## 🏗️ Estructura de Archivos Creados

```
app/
├── models/
│   ├── usuarios.py         # Modelo de usuarios
│   └── auth.py            # Modelos de autenticación (tokens, sesiones, etc.)
├── schemas/
│   └── auth.py            # Esquemas Pydantic para autenticación
├── crud/
│   └── auth.py            # Operaciones CRUD de autenticación
├── routers/
│   ├── auth.py            # Endpoints de autenticación
│   └── users.py           # Endpoints de gestión de usuarios
├── utils/
│   ├── security.py        # Funciones de seguridad (hashing, tokens)
│   ├── jwt_handler.py     # Manejo de tokens JWT
│   ├── auth_dependencies.py # Dependencias de autenticación
│   └── email_service.py   # Servicio de emails (mock)
└── scripts/
    └── create_admin.py     # Script para crear admin por defecto
```

## 🔧 Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Edita el archivo `.env` con tus configuraciones:

```env
# Base de datos (PostgreSQL en producción)
DATABASE_URL=postgresql://usuario:password@host:port/database

# Clave secreta JWT (¡CAMBIAR EN PRODUCCIÓN!)
SECRET_KEY=tu-clave-secreta-muy-segura-de-al-menos-32-caracteres

# URL del frontend
FRONTEND_URL=https://tu-frontend.com

# Configuración de email (opcional)
SENDGRID_API_KEY=tu-api-key
FROM_EMAIL=noreply@tudominio.com
```

### 3. Crear las tablas de base de datos
Las tablas se crean automáticamente al ejecutar la aplicación, pero también puedes ejecutar el script SQL del documento `DATABASE_SCHEMA.md` directamente en PostgreSQL.

### 4. Crear usuario administrador
```bash
python -m app.scripts.create_admin
```

Esto creará el usuario por defecto:
- **Email**: admin@numismatica.com
- **Contraseña**: admin123
- **Rol**: super_admin

### 5. Ejecutar la aplicación
```bash
uvicorn app.main:app --reload
```

## 📖 Uso de la API

### Ejemplo: Login
```bash
curl -X POST "http://localhost:8000/auth/login/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@numismatica.com",
       "password": "admin123"
     }'
```

### Ejemplo: Acceder a endpoints protegidos
```bash
curl -X GET "http://localhost:8000/auth/me/" \
     -H "Authorization: Bearer tu-jwt-token-aqui"
```

### Ejemplo: Crear usuario (solo super_admin)
```bash
curl -X POST "http://localhost:8000/auth/users/" \
     -H "Authorization: Bearer tu-jwt-token" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "nuevo@usuario.com",
       "password": "MiPassword123",
       "nombre": "Nuevo",
       "apellidos": "Usuario",
       "role": "admin"
     }'
```

## 🔒 Roles y Permisos

### Roles Disponibles:
- **admin**: Puede gestionar usuarios y acceder a funciones administrativas
- **super_admin**: Puede crear/eliminar usuarios y cambiar roles

### Permisos por Endpoint:
- **Públicos**: `/auth/login/`, `/auth/forgot-password/`, `/auth/reset-password/`
- **Autenticados**: `/auth/me/`, `/auth/logout/`
- **Admin**: `/auth/users/*` (ver, editar, resetear contraseñas)
- **Super Admin**: Crear y eliminar usuarios, asignar rol super_admin

## 🛡️ Características de Seguridad Adicionales

### Rate Limiting
- Máximo 5 intentos de login fallidos por IP por hora
- Bloqueo temporal de usuario tras 5 intentos fallidos

### Validación de Contraseñas
- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 minúscula  
- Al menos 1 número

### Tokens de Recuperación
- Válidos por 24 horas únicamente
- Un solo uso
- Invalidación automática de tokens anteriores

### JWT
- Expiración: 30 minutos
- Algoritmo: HS256
- Incluye user_id y email en payload

## 🚀 Despliegue en Producción

### Variables de Entorno Críticas:
```env
SECRET_KEY=clave-super-segura-de-produccion
DATABASE_URL=postgresql://...
FRONTEND_URL=https://tu-dominio.com
```

### Recomendaciones:
1. **HTTPS obligatorio** en producción
2. **CORS restrictivo** - configura dominios específicos
3. **Rate limiting** a nivel de servidor (Nginx/CloudFlare)
4. **Monitoreo** de intentos de login fallidos
5. **Backup** regular de la base de datos
6. **Logs** de seguridad activados

## 📧 Configuración de Email (Producción)

Para enviar emails reales de recuperación, configura un proveedor:

### SendGrid (Recomendado):
```bash
pip install sendgrid
```

```env
SENDGRID_API_KEY=tu-api-key
FROM_EMAIL=noreply@tudominio.com
```

### AWS SES, Mailgun, etc.
Modifica el archivo `app/utils/email_service.py` según tu proveedor.

## 🧪 Testing

Los endpoints están listos para testing. Puedes usar:
- **Postman** - Importa la colección de endpoints
- **pytest** - Para testing automatizado
- **FastAPI Docs** - http://localhost:8000/docs

## ❓ Resolución de Problemas

### Token inválido:
- Verifica que el token no haya expirado
- Asegúrate de incluir "Bearer " antes del token

### Usuario bloqueado:
- Espera 1 hora o resetea desde admin
- Verifica que `bloqueado_hasta` sea NULL en la BD

### Error de base de datos:
- Verifica la cadena de conexión `DATABASE_URL`
- Ejecuta las migraciones de tablas

¡El sistema de autenticación está completo y listo para usar! 🎉