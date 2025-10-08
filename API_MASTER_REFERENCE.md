# 🚀 API REFERENCE - SISTEMA DE BILLETES

**Última Actualización:** 08 de octubre de 2025
**Versión API:** 1.5.0  
**Base URL:** `https://fastapi-railway-ihky.onrender.com`  

---

## 📊 **ÍNDICE DE ENDPOINTS**

| Endpoint | Método | Autenticación | Descripción |
|----------|--------|---------------|-------------|
| [🏦 Billetes](#-billetes) | | | |
| `/billetes/` | GET | ❌ No | Lista billetes con filtros |
| `/billetes/{id}` | GET | ❌ No | Obtener billete por ID |
| `/billetes/` | POST | ✅ Sí | Crear nuevo billete |
| `/billetes/{id}` | PUT | ✅ Sí | Actualizar billete |
| `/billetes/{id}` | DELETE | ✅ Sí | Eliminar billete |
| `/billetes/{id}/destacado` | PATCH | ✅ Sí | Marcar/desmarcar destacado |
| `/billetes/{id}/vendido` | PATCH | ✅ Sí | Marcar/desmarcar vendido |
| `/billetes/stats` | GET | ❌ No | Estadísticas generales |
| [🏷️ Características](#️-características) | | | |
| `/billetes/caracteristicas/` | GET | ❌ No | Lista características |
| `/billetes/caracteristicas/` | POST | ✅ Sí | Crear característica |
| `/billetes/caracteristicas/{id}` | PUT | ✅ Sí | Actualizar característica |
| `/billetes/caracteristicas/{id}` | DELETE | ✅ Sí | Eliminar característica |
| [🌍 Países](#-países) | | | |
| `/paises/` | GET | ❌ No | Lista países |
| [🔐 Autenticación](#-autenticación) | | | |
| `/auth/login` | POST | ❌ No | Iniciar sesión |
| `/users/me` | GET | ✅ Sí | Perfil del usuario |
| `/users/me` | GET | ✅ Sí | Perfil del usuario |

---

## 🏦 **BILLETES**

### **📋 Listar Billetes**
```http
GET /billetes/
```

**Parámetros Query (todos opcionales):**
- `page` (int): Número de página - Default: 1
- `page_size` (int): Elementos por página - Default: 10, Max: 100
- `pais_id` (int): Filtrar por ID del país
- `denominacion` (str): Filtrar por denominación exacta
- `precio_min` (float): Precio mínimo
- `precio_max` (float): Precio máximo
- `estado` (str): `"Regular"` | `"Aceptable"` | `"Bueno"` | `"Muy bueno"` | `"Excelente"`
- `vendido` (bool): true/false
- `destacado` (bool): true/false
- `pick` (str): Código Pick del billete
- `banco_emisor` (str): Nombre del banco emisor
- `caracteristica_id` (int): ID de característica específica
- `search` (str): Búsqueda libre en denominación, banco_emisor, descripciones (incluyendo descripción general)

**Respuesta 200:**
```json
{
  "billetes": [
    {
      "id": 1,
      "pais": 1,
      "denominacion": "50000",
      "precio": "150000",
      "banco_emisor": "Banco de la República de Colombia",
      "medidas": "70 x 140 mm",
      "descripcion_anverso": "Retrato de Gabriel García Márquez...",
      "descripcion_reverso": "Escenas de Macondo...",
      "descripcion_general": "Billete conmemorativo del premio Nobel de Literatura...",
      "url_anverso": "https://example.com/anverso.jpg",
      "url_reverso": "https://example.com/reverso.jpg",
      "pick": "P-458",
      "estado": "Excelente",
      "vendido": false,
      "destacado": true,
      "fecha_actualizacion": "2025-10-07T10:30:00Z",
      "caracteristicas": [
        {
          "id": 1,
          "nombre": "Conmemorativo",
          "descripcion": "Billete conmemorativo especial",
          "color": "#007bff"
        }
      ],
      "pais_rel": {
        "id": 1,
        "pais": "Colombia",
        "bandera": "🇨🇴"
      }
    }
  ],
  "total": 156,
  "page": 1,
  "page_size": 10,
  "total_pages": 16,
  "has_next": true,
  "has_prev": false
}
```

---

### **🔍 Obtener Billete por ID**
```http
GET /billetes/{id}
```

**Parámetros URL:**
- `id` (int): ID del billete

**Respuesta 200:** (Mismo formato que un billete individual del listado)

**Errores:**
- `404`: Billete no encontrado

---

### **➕ Crear Billete**
```http
POST /billetes/
Authorization: Bearer {token}
Content-Type: application/json
```

**Cuerpo de la Petición:**
```json
{
  "pais": 1,
  "denominacion": "100000",
  "precio": "300000",
  "banco_emisor": "Banco Central",
  "medidas": "75 x 150 mm",
  "descripcion_anverso": "Descripción del frente",
  "descripcion_reverso": "Descripción del reverso",
  "descripcion_general": "Descripción general del billete y su contexto histórico",
  "url_anverso": "https://example.com/anverso.jpg",
  "url_reverso": "https://example.com/reverso.jpg",
  "pick": "P-123",
  "estado": "Muy bueno",
  "vendido": false,
  "destacado": true,
  "caracteristicas_ids": [1, 2]
}
```

**Campos Requeridos:**
- `pais` (int)
- `denominacion` (string, 1-100 chars)
- `precio` (string, 1-50 chars)

**Campos Opcionales:**
- `banco_emisor` (string, máx 255 chars)
- `medidas` (string, máx 50 chars)
- `descripcion_anverso` (text)
- `descripcion_reverso` (text)
- `descripcion_general` (text) **← NUEVO CAMPO**
- `url_anverso` (string)
- `url_reverso` (string)
- `pick` (string, máx 50 chars)
- `estado` (enum: "Regular", "Aceptable", "Bueno", "Muy bueno", "Excelente")
- `vendido` (boolean)
- `destacado` (boolean)
- `caracteristicas_ids` (array de integers)

**Respuesta 201:** (Billete creado con ID asignado)

**Errores:**
- `401`: No autenticado
- `422`: Error de validación

---

### **✏️ Actualizar Billete**
```http
PUT /billetes/{id}
Authorization: Bearer {token}
Content-Type: application/json
```

**Cuerpo:** (Mismo formato que POST, todos los campos opcionales)

**Respuesta 200:** (Billete actualizado)

**Errores:**
- `401`: No autenticado
- `404`: Billete no encontrado
- `422`: Error de validación

---

### **🗑️ Eliminar Billete**
```http
DELETE /billetes/{id}
Authorization: Bearer {token}
```

**Respuesta 204:** (Sin contenido)

**Errores:**
- `401`: No autenticado
- `404`: Billete no encontrado

---

### **⭐ Marcar/Desmarcar Destacado**
```http
PATCH /billetes/{id}/destacado
Authorization: Bearer {token}
Content-Type: application/json
```

**Parámetros URL:**
- `id` (int): ID del billete

**Cuerpo:**
```json
{
  "destacado": true  // boolean - true para destacar, false para quitar
}
```

**Respuesta 200:**
```json
{
  "id": 2,
  "destacado": true,
  "mensaje": "Billete marcado como destacado exitosamente",
  "fecha_actualizacion": "2025-10-07T15:30:00Z"
}
```

**Errores:**
- `401`: No autenticado
- `404`: Billete no encontrado
- `422`: Error de validación

---

### **💰 Marcar/Desmarcar Vendido**
```http
PATCH /billetes/{id}/vendido
Authorization: Bearer {token}
Content-Type: application/json
```

**Parámetros URL:**
- `id` (int): ID del billete

**Cuerpo:**
```json
{
  "vendido": false  // boolean - true para marcar vendido, false para disponible
}
```

**Respuesta 200:**
```json
{
  "id": 2,
  "vendido": false,
  "mensaje": "Billete marcado como disponible exitosamente",
  "fecha_actualizacion": "2025-10-07T15:30:00Z"
}
```

**Errores:**
- `401`: No autenticado
- `404`: Billete no encontrado
- `422`: Error de validación

---

### **📈 Estadísticas**
```http
GET /billetes/stats
```

**Respuesta 200:**
```json
{
  "total_billetes": 156,
  "total_vendidos": 23,
  "total_disponibles": 133,
  "total_destacados": 12,
  "valor_total_inventario": "45750000",
  "valor_inventario_disponible": "38900000",
  "estadisticas_por_pais": {
    "Colombia": {
      "total": 89,
      "vendidos": 12,
      "disponibles": 77,
      "valor_total": "25600000"
    }
  },
  "estadisticas_por_estado": {
    "Regular": 5,
    "Aceptable": 12,
    "Bueno": 78,
    "Muy bueno": 45,
    "Excelente": 67
  },
  "caracteristicas_mas_usadas": [
    {
      "caracteristica": "Histórico",
      "nombre": "Histórico",
      "color": "#28a745",
      "cantidad_billetes": 34
    }
  ]
}
```

---

## 🏷️ **CARACTERÍSTICAS**

### **📋 Listar Características**
```http
GET /caracteristicas/
```

**Parámetros Query:**
- `activo` (bool): Filtrar por características activas - Default: true

**Respuesta 200:**
```json
[
  {
    "id": 1,
    "nombre": "Conmemorativo",
    "descripcion": "Billete de emisión especial conmemorativa",
    "color": "#007bff",
    "fecha_creacion": "2025-10-07T10:00:00Z"
  }
]
```

---

### **➕ Crear Característica**
```http
POST /caracteristicas/
Authorization: Bearer {token}
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "nombre": "Nueva Característica",
  "descripcion": "Descripción opcional",
  "color": "#ff6b35"
}
```

**Campos Requeridos:**
- `nombre` (string, 1-100 chars, único)

**Campos Opcionales:**
- `descripcion` (string)
- `color` (string, formato hexadecimal #RRGGBB)

**Respuesta 201:** (Característica creada)

---

### **✏️ Actualizar Característica**
```http
PUT /caracteristicas/{id}
Authorization: Bearer {token}
Content-Type: application/json
```

**Cuerpo:** (Mismo formato que POST, todos campos opcionales)

**Respuesta 200:** (Característica actualizada)

---

### **🗑️ Eliminar Característica**
```http
DELETE /caracteristicas/{id}
Authorization: Bearer {token}
```

**Respuesta 204:** (Sin contenido)

**Nota:** No se puede eliminar si hay billetes asociados

---

## 🌍 **PAÍSES**

### **📋 Listar Países**
```http
GET /paises/
```

**Respuesta 200:**
```json
[
  {
    "id": 1,
    "pais": "Colombia",
    "bandera": "🇨🇴"
  },
  {
    "id": 2,
    "pais": "Argentina",
    "bandera": "🇦🇷"
  }
]
```

---

## 🔐 **AUTENTICACIÓN**

### **🔑 Iniciar Sesión**
```http
POST /auth/login
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "email": "admin@ejemplo.com",
  "password": "mi_password"
}
```

**Respuesta 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "admin@ejemplo.com",
    "nombre": "Administrador"
  }
}
```

**Errores:**
- `401`: Credenciales inválidas

---

### **👤 Perfil del Usuario**
```http
GET /users/me
Authorization: Bearer {token}
```

**Respuesta 200:**
```json
{
  "id": 1,
  "email": "admin@ejemplo.com",
  "nombre": "Administrador",
  "is_active": true,
  "fecha_creacion": "2025-01-01T00:00:00Z"
}
```

---

## ⚠️ **CÓDIGOS DE ERROR COMUNES**

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| `400` | Petición incorrecta | Parámetros inválidos |
| `401` | No autenticado | Token faltante/inválido |
| `403` | Sin permisos | Usuario sin privilegios |
| `404` | No encontrado | Recurso inexistente |
| `422` | Error de validación | Datos no válidos |
| `500` | Error del servidor | Error interno |

**Formato de Error:**
```json
{
  "detail": "Descripción del error"
}
```

**Error de Validación (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "denominacion"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🔧 **CONFIGURACIÓN**

### **📦 Headers Comunes:**
```http
Content-Type: application/json
Authorization: Bearer {jwt_token}  // Para endpoints protegidos
```

### **🚀 Rate Limiting:**
- No implementado actualmente
- Recomendado: 100 requests/minuto por IP

### **📄 Paginación:**
- Automática en todos los listados
- Máximo 100 elementos por página
- Headers de respuesta incluyen información de paginación

### **🔍 CORS:**
- Configurado para permitir todos los orígenes
- Métodos permitidos: GET, POST, PUT, DELETE, PATCH
- Headers permitidos: Authorization, Content-Type

---

## 📚 **DOCUMENTACIÓN ADICIONAL**

- **Swagger UI:** `https://fastapi-railway-ihky.onrender.com/docs`
- **ReDoc:** `https://fastapi-railway-ihky.onrender.com/redoc`
- **OpenAPI JSON:** `https://fastapi-railway-ihky.onrender.com/openapi.json`

---

## 📝 **CHANGELOG**

### **v1.5.0 - 8 de octubre de 2025**
- ✅ Actualizada escala de estados de billetes
- ✅ Nuevos estados: "Regular", "Aceptable", "Bueno", "Muy bueno", "Excelente"
- ✅ Migración automática de estados existentes
- ✅ Documentación actualizada con nueva escala de calidad

### **v1.4.0 - 7 de octubre de 2025**
- ✅ Agregado campo `descripcion_general` a la tabla billetes
- ✅ Actualizado esquemas de API para incluir descripción general
- ✅ Mejorado filtro de búsqueda para incluir descripción general
- ✅ Garantizado retorno de `fecha_actualizacion` en todas las respuestas
- ✅ Incluida migración de base de datos automática

### **v1.3.0 - 7 de octubre de 2025**
- ✅ Implementados endpoints PATCH para toggle de estados
- ✅ Agregado `/billetes/{id}/destacado` y `/billetes/{id}/vendido`
- ✅ Endpoint `/users/me` para perfil de usuario
- ✅ Endpoint `/billetes/stats` público mejorado
- ✅ Sistema de características completamente funcional
- ✅ Respuestas estructuradas para toggles con mensajes

### **v1.2.0 - 7 de octubre de 2025**
- ✅ Agregado sistema de características
- ✅ Nuevos campos en billetes (banco_emisor, medidas, etc.)
- ✅ Eliminados campos obsoletos (anverso, reverso)
- ✅ Endpoint de estadísticas
- ✅ Filtros avanzados y búsqueda
- ✅ Optimización de rendimiento con índices

### **v1.1.0 - Anterior**
- ✅ CRUD básico de billetes
- ✅ Sistema de autenticación JWT
- ✅ Relación con países

---

**🔄 Este documento se actualiza automáticamente con cada cambio en la API**