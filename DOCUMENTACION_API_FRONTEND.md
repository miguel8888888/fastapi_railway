# 📋 DOCUMENTACIÓN DE API - SISTEMA DE BILLETES ACTUALIZADO

## 🏗️ **RESUMEN DE CAMBIOS IMPLEMENTADOS**

### 🗄️ **MIGRACIÓN DE BASE DE DATOS**
- ✅ Agregadas **11 columnas nuevas** a la tabla `billetes`
- ❌ Eliminadas **2 columnas obsoletas** (`anverso`, `reverso`)
- ✅ Creada nueva tabla `caracteristicas` para clasificación
- ✅ Creada tabla de relación `billete_caracteristicas` (many-to-many)
- ✅ Agregados **5 índices** para optimización de consultas

---

## 📊 **ESQUEMA ACTUAL DE BASE DE DATOS**

### 🏦 **Tabla `billetes` (15 columnas)**

| Columna | Tipo | Descripción | Obligatorio |
|---------|------|-------------|-------------|
| `id` | INTEGER | ID único (autoincremental) | ✅ |
| `pais` | INTEGER | ID del país (FK a `paises`) | ✅ |
| `denominacion` | VARCHAR | Valor del billete | ✅ |
| `precio` | VARCHAR | Precio de venta | ✅ |
| `banco_emisor` | VARCHAR(255) | Nombre del banco emisor | ❌ |
| `medidas` | VARCHAR(50) | Dimensiones del billete | ❌ |
| `descripcion_anverso` | TEXT | Descripción del frente | ❌ |
| `descripcion_reverso` | TEXT | Descripción del reverso | ❌ |
| `url_anverso` | TEXT | URL imagen del frente | ❌ |
| `url_reverso` | TEXT | URL imagen del reverso | ❌ |
| `pick` | VARCHAR(50) | Código Pick del billete | ❌ |
| `estado` | VARCHAR(20) | Estado de conservación | ❌ |
| `vendido` | BOOLEAN | Si está vendido | ✅ (default: false) |
| `destacado` | BOOLEAN | Si es destacado | ✅ (default: false) |
| `fecha_actualizacion` | TIMESTAMP | Última actualización | ✅ (auto) |

### 🏷️ **Tabla `caracteristicas` (Nueva)**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INTEGER | ID único |
| `nombre` | VARCHAR(100) | Nombre de la característica |
| `descripcion` | TEXT | Descripción detallada |
| `color` | VARCHAR(7) | Color hexadecimal |
| `fecha_creacion` | TIMESTAMP | Fecha de creación |

### 🔗 **Tabla `billete_caracteristicas` (Relación)**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INTEGER | ID único |
| `billete_id` | INTEGER | ID del billete |
| `caracteristica_id` | INTEGER | ID de la característica |
| `fecha_creacion` | TIMESTAMP | Fecha de asociación |

---

## 🚀 **ENDPOINTS API DISPONIBLES**

### **BASE URL:** `https://fastapi-railway-ihky.onrender.com`

---

## 🏦 **ENDPOINTS DE BILLETES**

### **1. 📋 Listar Billetes con Filtros y Paginación**
```http
GET /billetes/?page=1&page_size=10&pais_id=1&destacado=true
```

**Parámetros de Query (todos opcionales):**
- `page` - Número de página (default: 1)
- `page_size` - Elementos por página (default: 10, max: 100)
- `pais_id` - Filtrar por país
- `denominacion` - Filtrar por denominación
- `precio_min` - Precio mínimo
- `precio_max` - Precio máximo  
- `estado` - Filtrar por estado: `"Excelente"`, `"Bueno"`, `"Regular"`, `"Malo"`
- `vendido` - true/false
- `destacado` - true/false
- `pick` - Código Pick
- `banco_emisor` - Nombre del banco
- `caracteristica_id` - Filtrar por característica específica
- `search` - Búsqueda de texto libre

**Respuesta:**
```json
{
  "billetes": [...],
  "total": 156,
  "page": 1,
  "page_size": 10,
  "total_pages": 16,
  "has_next": true,
  "has_prev": false
}
```

### **2. 🔍 Obtener Billete por ID**
```http
GET /billetes/{id}
```

**Respuesta:**
```json
{
  "id": 1,
  "pais": 1,
  "denominacion": "50000",
  "precio": "150000",
  "banco_emisor": "Banco de la República de Colombia",
  "medidas": "70 x 140 mm",
  "descripcion_anverso": "Retrato de Gabriel García Márquez...",
  "descripcion_reverso": "Escenas de Macondo...",
  "url_anverso": "https://example.com/anverso.jpg",
  "url_reverso": "https://example.com/reverso.jpg",
  "pick": "P-458",
  "estado": "Excelente",
  "vendido": false,
  "destacado": true,
  "fecha_actualizacion": "2025-10-06T15:30:00Z",
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
```

### **3. ➕ Crear Nuevo Billete** (Requiere Autenticación)
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
  "url_anverso": "https://example.com/anverso.jpg",
  "url_reverso": "https://example.com/reverso.jpg",
  "pick": "P-123",
  "estado": "Excelente",
  "vendido": false,
  "destacado": true,
  "caracteristicas_ids": [1, 2, 3]
}
```

### **4. ✏️ Actualizar Billete** (Requiere Autenticación)
```http
PUT /billetes/{id}
Authorization: Bearer {token}
```

### **5. 🗑️ Eliminar Billete** (Requiere Autenticación)
```http
DELETE /billetes/{id}
Authorization: Bearer {token}
```

### **6. ⭐ Marcar/Desmarcar como Destacado** (Requiere Autenticación)
```http
PATCH /billetes/{id}/destacado
Authorization: Bearer {token}
```

**Cuerpo:**
```json
{
  "destacado": true
}
```

### **7. 💰 Marcar/Desmarcar como Vendido** (Requiere Autenticación)
```http
PATCH /billetes/{id}/vendido
Authorization: Bearer {token}
```

---

## 🏷️ **ENDPOINTS DE CARACTERÍSTICAS**

### **8. 📋 Listar Características**
```http
GET /caracteristicas/?activo=true
```

### **9. ➕ Crear Característica** (Requiere Autenticación)
```http
POST /caracteristicas/
Authorization: Bearer {token}
```

**Cuerpo:**
```json
{
  "nombre": "Conmemorativo",
  "descripcion": "Billete de emisión especial",
  "color": "#ff6b35"
}
```

### **10. ✏️ Actualizar Característica** (Requiere Autenticación)
```http
PUT /caracteristicas/{id}
Authorization: Bearer {token}
```

### **11. 🗑️ Eliminar Característica** (Requiere Autenticación)
```http
DELETE /caracteristicas/{id}
Authorization: Bearer {token}
```

---

## 📊 **ENDPOINTS DE ESTADÍSTICAS**

### **12. 📈 Estadísticas Generales**
```http
GET /billetes/stats
```

**Respuesta:**
```json
{
  "total_billetes": 156,
  "total_vendidos": 23,
  "total_destacados": 12,
  "valor_inventario": "15750000",
  "por_pais": {
    "Colombia": 89,
    "Argentina": 45,
    "Brasil": 22
  },
  "por_estado": {
    "Excelente": 67,
    "Bueno": 78,
    "Regular": 11
  }
}
```

---

## 🔐 **AUTENTICACIÓN**

Los endpoints marcados con **(Requiere Autenticación)** necesitan:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Para obtener el token, usar:
```http
POST /auth/login
Content-Type: application/json

{
  "email": "admin@ejemplo.com",
  "password": "mi_password"
}
```

---

## ⚡ **OPTIMIZACIONES IMPLEMENTADAS**

### 🚀 **Rendimiento**
- ✅ **Paginación automática** (max 100 elementos por página)
- ✅ **Índices en columnas frecuentes** (`pais`, `vendido`, `destacado`, `denominacion`, `pick`)
- ✅ **Joins optimizados** con `joinedload` para relaciones
- ✅ **Filtros eficientes** con SQLAlchemy

### 🔍 **Búsquedas Avanzadas**
- ✅ **Búsqueda de texto libre** en `denominacion`, `banco_emisor`, descripciones
- ✅ **Filtros combinables** (todos los parámetros se pueden usar juntos)
- ✅ **Ordenamiento automático** por fecha de actualización

---

## 🎨 **ESTADOS VÁLIDOS**

### 📊 **Estados de Conservación:**
- `"Excelente"` - Billete en perfectas condiciones
- `"Bueno"` - Billete con mínimo uso
- `"Regular"` - Billete con uso moderado
- `"Malo"` - Billete muy usado

### 🏷️ **Campos Booleanos:**
- `vendido`: `true` = Vendido, `false` = Disponible
- `destacado`: `true` = Aparece en destacados, `false` = Normal

---

## 🌐 **CÓDIGOS DE RESPUESTA HTTP**

| Código | Significado |
|--------|-------------|
| `200` | ✅ Operación exitosa |
| `201` | ✅ Recurso creado |
| `400` | ❌ Datos inválidos |
| `401` | 🔒 No autenticado |
| `403` | 🚫 Sin permisos |
| `404` | 🔍 No encontrado |
| `422` | 📝 Error de validación |
| `500` | 💥 Error del servidor |

---

## 🔄 **CAMBIOS IMPORTANTES PARA EL FRONTEND**

### ❌ **CAMPOS ELIMINADOS (No usar más):**
- `anverso` - Reemplazado por `url_anverso` y `descripcion_anverso`
- `reverso` - Reemplazado por `url_reverso` y `descripcion_reverso`

### ✅ **NUEVOS CAMPOS DISPONIBLES:**
- `banco_emisor` - Nombre del banco que emitió el billete
- `medidas` - Dimensiones físicas
- `descripcion_anverso` - Descripción del diseño del frente
- `descripcion_reverso` - Descripción del diseño del reverso  
- `url_anverso` - URL de la imagen del frente
- `url_reverso` - URL de la imagen del reverso
- `pick` - Código de catálogo Pick
- `estado` - Estado de conservación
- `vendido` - Estado de venta
- `destacado` - Si aparece en destacados
- `fecha_actualizacion` - Timestamp de última actualización
- `caracteristicas` - Array de características asociadas

### 🔗 **NUEVAS RELACIONES:**
- Cada billete puede tener múltiples características
- Cada característica puede aplicar a múltiples billetes
- Relación con país incluye nombre y bandera

---

## 💡 **EJEMPLOS DE USO PARA EL FRONTEND**

### 🏠 **Página Principal - Billetes Destacados:**
```javascript
fetch('https://fastapi-railway-ihky.onrender.com/billetes/?destacado=true&page_size=6')
```

### 🔍 **Búsqueda con Filtros:**
```javascript
const params = new URLSearchParams({
    pais_id: 1,
    estado: 'Excelente',
    vendido: false,
    search: 'García Márquez',
    page: 1,
    page_size: 20
});

fetch(`https://fastapi-railway-ihky.onrender.com/billetes/?${params}`)
```

### 🏷️ **Mostrar Características:**
```javascript
// Las características vienen incluidas en cada billete
billete.caracteristicas.forEach(caracteristica => {
    console.log(`${caracteristica.nombre} - Color: ${caracteristica.color}`);
});
```

---

## 🚨 **NOTAS IMPORTANTES**

1. **Paginación Obligatoria:** Todos los listados están paginados automáticamente
2. **Autenticación JWT:** Los tokens expiran, implementar renovación automática
3. **Validation:** Todos los campos tienen validación estricta en el backend
4. **CORS:** Configurado para permitir requests desde cualquier origen
5. **Rate Limiting:** No implementado aún, pero recomendado para producción

---

## 🛠️ **HERRAMIENTAS DE DESARROLLO**

### 📚 **Documentación Interactiva:**
- Swagger UI: `https://fastapi-railway-ihky.onrender.com/docs`
- ReDoc: `https://fastapi-railway-ihky.onrender.com/redoc`

### 🧪 **Testing:**
- Todos los endpoints tienen tests automatizados
- Base de datos de prueba con datos de ejemplo disponibles

---

**📅 Última actualización:** 6 de octubre de 2025  
**🔄 Versión API:** 1.2.0  
**📧 Contacto:** Para dudas sobre la API, contactar al equipo de backend