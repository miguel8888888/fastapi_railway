# 🔧 REQUERIMIENTOS DE APIs FALTANTES PARA EL BACKEND

**Fecha:** 7 de octubre de 2025  
**Versión:** 1.0  
**Estado:** Pendiente de implementación  
**Base URL:** `https://fastapi-railway-ihky.onrender.com`

---

## 📋 **RESUMEN EJECUTIVO**

El frontend está completamente implementado pero **8 endpoints críticos** faltan en el backend. Estos endpoints son esenciales para:
- ✅ Gestión de estados de billetes (destacado/vendido)
- ✅ Sistema completo de características
- ✅ Estadísticas del inventario
- ✅ Perfil de usuario

**Prioridad de implementación:**
- 🔴 **CRÍTICA:** Endpoints PATCH para toggles de billetes
- 🟡 **ALTA:** Sistema de características completo
- 🟢 **MEDIA:** Estadísticas y perfil de usuario

---

## 🚨 **APIS CRÍTICAS FALTANTES**

### 🔴 **1. PATCH /billetes/{id}/destacado**

**Descripción:** Toggle del estado destacado de un billete de forma eficiente.

**Especificación técnica:**
```http
PATCH /billetes/{id}/destacado
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "destacado": true  // boolean - true para destacar, false para quitar
}
```

**Response 200 (Éxito):**
```json
{
  "id": 2,
  "destacado": true,
  "mensaje": "Billete marcado como destacado exitosamente",
  "fecha_actualizacion": "2025-10-07T15:30:00Z"
}
```

**Validaciones requeridas:**
- ✅ Token JWT válido y activo
- ✅ El billete con `{id}` debe existir
- ✅ El campo `destacado` debe ser boolean
- ✅ Actualizar `fecha_actualizacion` automáticamente

**Códigos de error:**
```json
// 401 - No autenticado
{"detail": "Token inválido o expirado"}

// 404 - Billete no encontrado  
{"detail": "Billete con ID 123 no encontrado"}

// 422 - Validación fallida
{
  "detail": [
    {
      "loc": ["body", "destacado"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### 🔴 **2. PATCH /billetes/{id}/vendido**

**Descripción:** Toggle del estado de venta de un billete.

**Especificación técnica:**
```http
PATCH /billetes/{id}/vendido
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "vendido": false  // boolean - true para marcar vendido, false para disponible
}
```

**Response 200 (Éxito):**
```json
{
  "id": 2,
  "vendido": false,
  "mensaje": "Billete marcado como disponible exitosamente",
  "fecha_actualizacion": "2025-10-07T15:30:00Z"
}
```

**Validaciones requeridas:**
- ✅ Token JWT válido y activo
- ✅ El billete con `{id}` debe existir
- ✅ El campo `vendido` debe ser boolean
- ✅ Actualizar `fecha_actualizacion` automáticamente

**Códigos de error:** (Idénticos al endpoint anterior)

---

### 🔴 **3. GET /caracteristicas/**

**Descripción:** Obtener lista de todas las características disponibles.

**Especificación técnica:**
```http
GET /caracteristicas/
```

**Query Parameters (Opcionales):**
```
?activo=true   // boolean - filtrar por características activas (default: true)
```

**Response 200 (Éxito):**
```json
[
  {
    "id": 1,
    "nombre": "Conmemorativo",
    "descripcion": "Billete de emisión especial conmemorativa",
    "color": "#007bff",
    "fecha_creacion": "2025-10-01T10:00:00Z"
  },
  {
    "id": 2,
    "nombre": "Raro",
    "descripcion": "Billete poco común en el mercado",
    "color": "#dc3545",
    "fecha_creacion": "2025-10-02T11:30:00Z"
  }
]
```

**Validaciones requeridas:**
- ✅ Ordenar por `fecha_creacion DESC`
- ✅ Filtrar por `activo=true` por defecto
- ✅ Retornar array vacío si no hay características

**Códigos de error:**
```json
// 500 - Error interno
{"detail": "Error interno del servidor"}
```

---

## 🟡 **APIS DE ALTA PRIORIDAD**

### 🟡 **4. POST /caracteristicas/**

**Descripción:** Crear una nueva característica para billetes.

**Especificación técnica:**
```http
POST /caracteristicas/
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "nombre": "Serie Limitada",           // REQUERIDO - string, 1-100 chars, único
  "descripcion": "Tirada limitada",    // OPCIONAL - string, max 500 chars
  "color": "#ffc107"                   // OPCIONAL - string, formato #RRGGBB
}
```

**Response 201 (Creado):**
```json
{
  "id": 3,
  "nombre": "Serie Limitada",
  "descripcion": "Tirada limitada",
  "color": "#ffc107",
  "fecha_creacion": "2025-10-07T15:45:00Z"
}
```

**Validaciones requeridas:**
- ✅ `nombre` único en la tabla
- ✅ `color` debe coincidir con regex: `^#[0-9A-Fa-f]{6}$`
- ✅ Auto-generar `fecha_creacion`
- ✅ Trimear espacios en `nombre` y `descripcion`

**Códigos de error:**
```json
// 401 - No autenticado
{"detail": "Token requerido"}

// 422 - Validación fallida
{
  "detail": [
    {
      "loc": ["body", "nombre"],
      "msg": "Ya existe una característica con este nombre",
      "type": "value_error.duplicate"
    }
  ]
}

// 422 - Color inválido
{
  "detail": [
    {
      "loc": ["body", "color"],
      "msg": "Formato de color inválido. Use formato #RRGGBB",
      "type": "value_error.invalid_format"
    }
  ]
}
```

---

### 🟡 **5. PUT /caracteristicas/{id}**

**Descripción:** Actualizar una característica existente.

**Especificación técnica:**
```http
PUT /caracteristicas/{id}
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body (Todos los campos opcionales):**
```json
{
  "nombre": "Nuevo Nombre",
  "descripcion": "Nueva descripción", 
  "color": "#28a745"
}
```

**Response 200 (Actualizado):**
```json
{
  "id": 1,
  "nombre": "Nuevo Nombre",
  "descripcion": "Nueva descripción",
  "color": "#28a745",
  "fecha_creacion": "2025-10-01T10:00:00Z"  // No cambia
}
```

**Validaciones requeridas:**
- ✅ La característica con `{id}` debe existir
- ✅ Si se envía `nombre`, debe ser único (excepto el actual)
- ✅ Validar formato de `color` si se envía
- ✅ NO actualizar `fecha_creacion`

---

### 🟡 **6. DELETE /caracteristicas/{id}**

**Descripción:** Eliminar una característica (solo si no tiene billetes asociados).

**Especificación técnica:**
```http
DELETE /caracteristicas/{id}
Authorization: Bearer {jwt_token}
```

**Response 204 (Eliminado):**
```
HTTP 204 No Content
(Sin cuerpo de respuesta)
```

**Validaciones requeridas:**
- ✅ La característica con `{id}` debe existir
- ✅ NO debe tener billetes asociados
- ✅ Eliminación física (no lógica)

**Códigos de error:**
```json
// 400 - No se puede eliminar
{
  "detail": "No se puede eliminar la característica. Tiene 5 billetes asociados."
}

// 404 - No encontrada
{
  "detail": "Característica con ID 123 no encontrada"
}
```

---

### 🟡 **7. GET /billetes/stats**

**Descripción:** Estadísticas completas del inventario de billetes.

**Especificación técnica:**
```http
GET /billetes/stats
```

**Response 200 (Éxito):**
```json
{
  "total_billetes": 156,
  "total_vendidos": 23,
  "total_disponibles": 133,
  "total_destacados": 12,
  "valor_total_inventario": "45750000.00",
  "valor_inventario_disponible": "38900000.00",
  "estadisticas_por_pais": {
    "Colombia": {
      "total": 89,
      "vendidos": 12,
      "disponibles": 77,
      "valor_total": "25600000.00"
    },
    "Argentina": {
      "total": 34,
      "vendidos": 8,
      "disponibles": 26,
      "valor_total": "8900000.00"
    }
  },
  "estadisticas_por_estado": {
    "Excelente": 67,
    "Bueno": 78,
    "Regular": 11,
    "Malo": 0
  },
  "caracteristicas_mas_usadas": [
    {
      "caracteristica": "Histórico",
      "nombre": "Histórico", 
      "color": "#28a745",
      "cantidad_billetes": 34
    },
    {
      "caracteristica": "Conmemorativo",
      "nombre": "Conmemorativo",
      "color": "#007bff", 
      "cantidad_billetes": 28
    }
  ]
}
```

**Cálculos requeridos:**
- ✅ `total_billetes`: COUNT de todos los billetes
- ✅ `total_vendidos`: COUNT WHERE vendido = true
- ✅ `total_disponibles`: COUNT WHERE vendido = false
- ✅ `total_destacados`: COUNT WHERE destacado = true
- ✅ `valor_total_inventario`: SUM(precio) de todos
- ✅ `valor_inventario_disponible`: SUM(precio) WHERE vendido = false
- ✅ Agrupar por país con JOINs
- ✅ Agrupar por estado
- ✅ Top 10 características más usadas

---

## 🟢 **APIS DE PRIORIDAD MEDIA**

### 🟢 **8. GET /users/me**

**Descripción:** Obtener perfil del usuario autenticado.

**Especificación técnica:**
```http
GET /users/me
Authorization: Bearer {jwt_token}
```

**Response 200 (Éxito):**
```json
{
  "id": 1,
  "email": "admin@numismatica.com",
  "nombre": "Administrador Principal",
  "is_active": true,
  "fecha_creacion": "2025-01-01T00:00:00Z",
  "ultimo_acceso": "2025-10-07T15:30:00Z"
}
```

**Validaciones requeridas:**
- ✅ Token JWT válido
- ✅ Usuario debe estar activo (`is_active = true`)
- ✅ Actualizar `ultimo_acceso` con timestamp actual

**Códigos de error:**
```json
// 401 - Token inválido
{"detail": "Token inválido o expirado"}

// 403 - Usuario inactivo
{"detail": "Usuario desactivado"}
```

---

## 🔧 **CONSIDERACIONES TÉCNICAS**

### **Autenticación JWT:**
```python
# Todas las rutas protegidas deben validar:
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validar token
    # Verificar expiración
    # Retornar usuario o lanzar HTTPException
```

### **Manejo de errores estándar:**
```python
from fastapi import HTTPException

# 401 - No autenticado
raise HTTPException(status_code=401, detail="Token inválido")

# 404 - Recurso no encontrado
raise HTTPException(status_code=404, detail="Billete no encontrado")

# 422 - Error de validación
raise HTTPException(status_code=422, detail=validation_errors)
```

### **Formato de timestamps:**
```python
# Usar ISO 8601 con timezone UTC
"fecha_creacion": "2025-10-07T15:30:00.000000Z"
```

### **Formato de valores monetarios:**
```python
# Strings con formato decimal para evitar problemas de precisión
"precio": "150000.00"
"valor_total": "45750000.00"
```

---

## 📊 **ESQUEMA DE BASE DE DATOS SUGERIDO**

### **Tabla: características**
```sql
CREATE TABLE caracteristicas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    color VARCHAR(7), -- formato #RRGGBB
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    activo BOOLEAN DEFAULT TRUE
);
```

### **Tabla: billete_caracteristicas (Many-to-Many)**
```sql
CREATE TABLE billete_caracteristicas (
    billete_id INTEGER REFERENCES billetes(id) ON DELETE CASCADE,
    caracteristica_id INTEGER REFERENCES caracteristicas(id) ON DELETE CASCADE,
    PRIMARY KEY (billete_id, caracteristica_id)
);
```

### **Índices recomendados:**
```sql
-- Para mejorar performance de consultas
CREATE INDEX idx_billetes_vendido ON billetes(vendido);
CREATE INDEX idx_billetes_destacado ON billetes(destacado);
CREATE INDEX idx_billetes_pais ON billetes(pais);
CREATE INDEX idx_caracteristicas_activo ON caracteristicas(activo);
```

---

## ✅ **CRITERIOS DE ACEPTACIÓN**

### **Para cada endpoint:**
1. ✅ Responde según la especificación exacta
2. ✅ Maneja todos los códigos de error documentados
3. ✅ Valida autenticación cuando es requerida
4. ✅ Incluye validaciones de entrada
5. ✅ Retorna timestamps en formato ISO 8601
6. ✅ Usa transacciones para operaciones críticas

### **Pruebas requeridas:**
1. ✅ Unit tests para cada endpoint
2. ✅ Integration tests con base de datos
3. ✅ Tests de autenticación
4. ✅ Tests de validación de entrada
5. ✅ Tests de manejo de errores

---

## 🚀 **PLAN DE IMPLEMENTACIÓN SUGERIDO**

### **Fase 1 - Crítico (1-2 días):**
1. `PATCH /billetes/{id}/destacado`
2. `PATCH /billetes/{id}/vendido`

### **Fase 2 - Alta prioridad (2-3 días):**
1. `GET /caracteristicas/`
2. `POST /caracteristicas/`
3. Crear tablas de características

### **Fase 3 - Completar sistema (1-2 días):**
1. `PUT /caracteristicas/{id}`
2. `DELETE /caracteristicas/{id}`
3. `GET /billetes/stats`
4. `GET /users/me`

### **Fase 4 - Testing y optimización (1 día):**
1. Tests completos
2. Optimización de queries
3. Documentación en Swagger

---

## 📞 **CONTACTO Y SEGUIMIENTO**

**Desarrollador Frontend:** Miguel  
**Documento creado:** 7 de octubre de 2025  
**Prioridad:** Crítica - Sistema bloqueado sin estos endpoints  

**Estado actual del frontend:** ✅ Completamente implementado y listo  
**Estado actual del backend:** ❌ Bloqueado - APIs faltantes  

---

**📋 Este documento debe ser implementado COMPLETO para que el sistema funcione correctamente.**