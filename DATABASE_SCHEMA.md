# 🗄️ Estructura de Base de Datos - Sistema de Autenticación

## 📋 **Tablas necesarias para el sistema de autenticación:**

### 1. 👥 **Tabla: `usuarios`** (PostgreSQL)
```sql
-- Crear extension para UUID si no existe
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tipo enum para roles
CREATE TYPE user_role AS ENUM ('admin', 'super_admin');

-- Crear tabla usuarios
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    role user_role DEFAULT 'admin',
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP NULL,
    intentos_login INTEGER DEFAULT 0,
    bloqueado_hasta TIMESTAMP NULL
);

-- Crear índices
CREATE INDEX idx_usuarios_email ON usuarios (email);
CREATE INDEX idx_usuarios_activo ON usuarios (activo);
CREATE INDEX idx_usuarios_role ON usuarios (role);

-- Crear función para actualizar fecha_actualizacion automáticamente
CREATE OR REPLACE FUNCTION update_fecha_actualizacion_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.fecha_actualizacion = NOW(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

-- Crear trigger para actualizar automáticamente fecha_actualizacion
CREATE TRIGGER update_usuarios_fecha_actualizacion 
    BEFORE UPDATE ON usuarios 
    FOR EACH ROW 
    EXECUTE FUNCTION update_fecha_actualizacion_column();
```

### 2. 🔑 **Tabla: `tokens_recuperacion`** (PostgreSQL)
```sql
CREATE TABLE tokens_recuperacion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    fecha_expiracion TIMESTAMP NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_solicitante INET,
    user_agent TEXT,
    
    CONSTRAINT fk_tokens_usuario FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Crear índices
CREATE INDEX idx_tokens_token ON tokens_recuperacion (token);
CREATE INDEX idx_tokens_usuario_id ON tokens_recuperacion (usuario_id);
CREATE INDEX idx_tokens_fecha_expiracion ON tokens_recuperacion (fecha_expiracion);
CREATE INDEX idx_tokens_usado ON tokens_recuperacion (usado);
```

### 3. 📝 **Tabla: `sesiones`** (PostgreSQL - Opcional)
```sql
CREATE TABLE sesiones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL,
    token_jwt TEXT NOT NULL,
    ip_address INET,
    user_agent TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT fk_sesiones_usuario FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Crear índices
CREATE INDEX idx_sesiones_usuario_id ON sesiones (usuario_id);
CREATE INDEX idx_sesiones_fecha_expiracion ON sesiones (fecha_expiracion);
CREATE INDEX idx_sesiones_activa ON sesiones (activa);
```

### 4. 🔐 **Tabla: `intentos_login`** (PostgreSQL - Opcional)
```sql
CREATE TABLE intentos_login (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    ip_address INET,
    exitoso BOOLEAN DEFAULT FALSE,
    fecha_intento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    mensaje VARCHAR(255)
);

-- Crear índices
CREATE INDEX idx_intentos_email ON intentos_login (email);
CREATE INDEX idx_intentos_ip_address ON intentos_login (ip_address);
CREATE INDEX idx_intentos_fecha_intento ON intentos_login (fecha_intento);
CREATE INDEX idx_intentos_exitoso ON intentos_login (exitoso);
```

## 🚀 **Scripts de inicialización:**

### **Usuario administrador por defecto:** (PostgreSQL)
```sql
-- Insertar usuario admin por defecto (la contraseña debe ser hasheada en el backend)
INSERT INTO usuarios (email, password_hash, nombre, role, activo) 
VALUES (
    'admin@numismatica.com', 
    '$2b$12$LQV3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeG7WBoWWDgdTZEm6', -- Hash de "admin123"
    'Administrador', 
    'super_admin', 
    TRUE
);
```

### **Limpieza automática de tokens expirados:** (PostgreSQL)
```sql
-- Función para limpiar tokens expirados
CREATE OR REPLACE FUNCTION limpiar_tokens_expirados()
RETURNS void AS $$
BEGIN
    DELETE FROM tokens_recuperacion 
    WHERE fecha_expiracion < NOW() OR usado = TRUE;
END;
$$ LANGUAGE plpgsql;

-- Si tienes extensión pg_cron instalada (opcional):
-- SELECT cron.schedule('limpiar-tokens', '0 * * * *', 'SELECT limpiar_tokens_expirados();');

-- Alternativamente, puedes crear un trabajo manual o usar un cron del sistema
-- Para ejecutar manualmente: SELECT limpiar_tokens_expirados();
```

## 🔧 **Endpoints de API necesarios:**

### **1. Autenticación:**
- `POST /auth/login/` - Login de usuario
- `POST /auth/logout/` - Cerrar sesión
- `POST /auth/refresh/` - Renovar token JWT

### **2. Recuperación de contraseña:**
- `POST /auth/forgot-password/` - Solicitar recuperación
- `POST /auth/reset-password/` - Resetear contraseña con token
- `GET /auth/verify-token/{token}` - Verificar token de recuperación

### **3. Gestión de usuarios (Admin):**
- `GET /auth/users/` - Listar usuarios
- `POST /auth/users/` - Crear usuario
- `PUT /auth/users/{id}` - Actualizar usuario
- `DELETE /auth/users/{id}` - Eliminar usuario
- `POST /auth/users/{id}/reset-password` - Resetear contraseña de usuario

## 🛡️ **Consideraciones de seguridad:**

### **Implementadas en el frontend:**
✅ Validación de formularios
✅ Sanitización de inputs
✅ Manejo seguro de tokens JWT
✅ Timeout de sesión
✅ Protección contra XSS básica

### **Requeridas en el backend:**
🔐 **Hashing de contraseñas:** bcrypt con salt rounds ≥ 12
🔐 **JWT seguro:** Firma con clave secreta fuerte, expiración corta
🔐 **Rate limiting:** Máximo 5 intentos de login por IP/hora
🔐 **Tokens de recuperación:** Expiran en 24 horas, solo un uso
🔐 **Validación de entrada:** Sanitización contra SQL injection
🔐 **HTTPS obligatorio:** Todas las comunicaciones encriptadas
🔐 **Headers de seguridad:** CORS, CSP, X-Frame-Options

## 📱 **URLs de acceso:**

### **Público:**
- `http://localhost:4200/` → Landing page

### **Autenticación:**
- `http://localhost:4200/auth/login` → Login
- `http://localhost:4200/auth/forgot-password` → Recuperar contraseña

### **Administración (requiere login):**
- `http://localhost:4200/admin` → Dashboard (redirige desde login exitoso)
- `http://localhost:4200/admin/dashboard` → Panel principal
- `http://localhost:4200/admin/registrar-paises` → Gestión de países

---

## 🎯 **Próximos pasos sugeridos:**

1. **Crear las tablas** en tu base de datos
2. **Implementar endpoints** de autenticación en FastAPI
3. **Crear usuario admin** por defecto
4. **Implementar AuthGuard** en Angular para proteger rutas admin
5. **Configurar interceptor HTTP** para incluir JWT en requests
6. **Implementar logout** y manejo de expiración de tokens
7. **Testing de seguridad** básico

¿Te ayudo con la implementación de alguno de estos pasos o quieres ajustar algo de la estructura propuesta?