# Sistema de Gestión de Billetes - Documentación del Backend

## Resumen

Este documento especifica los requisitos del backend para el sistema expandido de gestión de billetes, que incluye nuevas funcionalidades para administrar características, estados avanzados y relaciones complejas entre billetes y sus atributos.

## Estructura de Base de Datos Expandida

### Tabla: billetes (actualizada)

```sql
CREATE TABLE billetes (
    id SERIAL PRIMARY KEY,
    pais_id INTEGER REFERENCES paises(id) ON DELETE CASCADE,
    banco_emisor VARCHAR(255),
    denominacion VARCHAR(100) NOT NULL,
    medidas VARCHAR(50), -- Ej: "140 x 70 mm"
    descripcion TEXT,
    descripcion_anverso TEXT,
    descripcion_reverso TEXT,
    url_anverso TEXT,
    url_reverso TEXT,
    pick VARCHAR(50), -- Código Pick del billete
    estado VARCHAR(20), -- UNC, AU, XF, VF, F, VG, G, P
    precio DECIMAL(10,2),
    vendido BOOLEAN DEFAULT FALSE,
    destacado BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Nueva Tabla: caracteristicas

```sql
CREATE TABLE caracteristicas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    color VARCHAR(7) DEFAULT '#3B82F6', -- Color hex para la UI
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Nueva Tabla: billete_caracteristicas (relación muchos a muchos)

```sql
CREATE TABLE billete_caracteristicas (
    id SERIAL PRIMARY KEY,
    billete_id INTEGER REFERENCES billetes(id) ON DELETE CASCADE,
    caracteristica_id INTEGER REFERENCES caracteristicas(id) ON DELETE CASCADE,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(billete_id, caracteristica_id)
);
```

### Datos Iniciales para Características

```sql
INSERT INTO caracteristicas (nombre, descripcion, color) VALUES
('Papel moneda', 'Billete impreso en papel tradicional', '#10B981'),
('Polímero', 'Billete de material plástico duradero', '#3B82F6'),
('Serie especial', 'Edición limitada o conmemorativa', '#F59E0B'),
('Sin circular', 'Billete en condición perfecta (UNC)', '#EF4444'),
('Marca de agua', 'Con marca de agua visible al trasluz', '#8B5CF6'),
('Holograma', 'Incluye elementos holográficos de seguridad', '#EC4899'),
('Microimpresión', 'Contiene texto microscópico de seguridad', '#6B7280'),
('Serie numerada', 'Billete con numeración específica', '#14B8A6'),
('Error de impresión', 'Billete con errores que lo hacen valioso', '#F97316'),
('Firma especial', 'Con firma de funcionario específico', '#84CC16');
```

## Endpoints del API

### Billetes

#### GET /api/billetes/
**Descripción**: Obtener lista de billetes con filtros y paginación
**Parámetros de consulta**:
- `page` (int, opcional): Página actual (default: 1)
- `limit` (int, opcional): Elementos por página (default: 10, max: 100)
- `search` (string, opcional): Búsqueda en denominación, descripción, pick
- `pais_id` (int, opcional): Filtrar por país
- `vendido` (boolean, opcional): Filtrar por estado de venta
- `destacado` (boolean, opcional): Filtrar por destacados
- `caracteristica_id` (int, opcional): Filtrar por característica
- `precio_min` (decimal, opcional): Precio mínimo
- `precio_max` (decimal, opcional): Precio máximo
- `estado` (string, opcional): Estado del billete (UNC, AU, XF, etc.)
- `order_by` (string, opcional): Campo de ordenación (precio, fecha_creacion, denominacion)
- `order` (string, opcional): Dirección (asc, desc)

**Respuesta**:
```json
{
  "items": [
    {
      "id": 1,
      "pais_id": 1,
      "pais": {
        "id": 1,
        "pais": "Colombia",
        "bandera": "co"
      },
      "banco_emisor": "Banco de la República",
      "denominacion": "50000 Pesos",
      "medidas": "140 x 70 mm",
      "descripcion": "Billete conmemorativo...",
      "descripcion_anverso": "Retrato de Gabriel García Márquez...",
      "descripcion_reverso": "Paisaje del Caribe colombiano...",
      "url_anverso": "https://storage.url/anverso.jpg",
      "url_reverso": "https://storage.url/reverso.jpg",
      "pick": "P-451",
      "estado": "UNC",
      "precio": 25.50,
      "vendido": false,
      "destacado": true,
      "caracteristicas": [
        {
          "id": 1,
          "nombre": "Polímero",
          "descripcion": "Material plástico",
          "color": "#3B82F6"
        }
      ],
      "fecha_creacion": "2024-01-15T10:30:00Z",
      "fecha_actualizacion": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 47,
    "items_per_page": 10,
    "has_next": true,
    "has_previous": false
  }
}
```

#### POST /api/billetes/
**Descripción**: Crear nuevo billete
**Body**:
```json
{
  "pais_id": 1,
  "banco_emisor": "Banco Central",
  "denominacion": "100 Euros",
  "medidas": "147 x 82 mm",
  "descripcion": "Billete de 100 euros...",
  "descripcion_anverso": "Retrato arquitectónico...",
  "descripcion_reverso": "Puente moderno...",
  "url_anverso": "https://storage.url/anverso.jpg",
  "url_reverso": "https://storage.url/reverso.jpg",
  "pick": "P-123",
  "estado": "XF",
  "precio": 120.00,
  "vendido": false,
  "destacado": false,
  "caracteristicas_ids": [1, 3, 5]
}
```

#### PUT /api/billetes/{id}/
**Descripción**: Actualizar billete completo
**Body**: Igual que POST

#### PATCH /api/billetes/{id}/
**Descripción**: Actualización parcial de billete
**Body**: Campos a actualizar

#### DELETE /api/billetes/{id}/
**Descripción**: Eliminar billete

#### GET /api/billetes/{id}/
**Descripción**: Obtener billete específico

#### POST /api/billetes/{id}/toggle-vendido/
**Descripción**: Cambiar estado de vendido
**Respuesta**:
```json
{
  "id": 1,
  "vendido": true,
  "mensaje": "Estado actualizado correctamente"
}
```

#### POST /api/billetes/{id}/toggle-destacado/
**Descripción**: Cambiar estado de destacado
**Respuesta**:
```json
{
  "id": 1,
  "destacado": false,
  "mensaje": "Estado actualizado correctamente"
}
```

### Características

#### GET /api/caracteristicas/
**Descripción**: Obtener todas las características
**Parámetros de consulta**:
- `activo` (boolean, opcional): Filtrar por activas/inactivas

**Respuesta**:
```json
{
  "items": [
    {
      "id": 1,
      "nombre": "Polímero",
      "descripcion": "Material plástico duradero",
      "color": "#3B82F6",
      "activo": true,
      "billetes_count": 15,
      "fecha_creacion": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### POST /api/caracteristicas/
**Descripción**: Crear nueva característica
**Body**:
```json
{
  "nombre": "Nueva característica",
  "descripcion": "Descripción opcional",
  "color": "#10B981",
  "activo": true
}
```

#### PUT /api/caracteristicas/{id}/
**Descripción**: Actualizar característica

#### DELETE /api/caracteristicas/{id}/
**Descripción**: Eliminar característica (solo si no tiene billetes asociados)

### Estadísticas y Reportes

#### GET /api/billetes/estadisticas/
**Descripción**: Obtener estadísticas generales
**Respuesta**:
```json
{
  "total_billetes": 147,
  "total_disponibles": 98,
  "total_vendidos": 49,
  "total_destacados": 23,
  "valor_total_coleccion": 12450.75,
  "valor_disponible": 8320.50,
  "valor_vendido": 4130.25,
  "billetes_por_pais": [
    {"pais": "España", "count": 45},
    {"pais": "Francia", "count": 32}
  ],
  "billetes_por_estado": [
    {"estado": "UNC", "count": 67},
    {"estado": "XF", "count": 45}
  ],
  "caracteristicas_mas_usadas": [
    {"nombre": "Polímero", "count": 34},
    {"nombre": "Marca de agua", "count": 78}
  ]
}
```

#### GET /api/billetes/por-pais/{pais_id}/
**Descripción**: Obtener billetes de un país específico

### Gestión de Imágenes

#### POST /api/upload/imagen/
**Descripción**: Subir imagen de billete
**Content-Type**: multipart/form-data
**Body**: archivo imagen (max 5MB, formatos: jpg, jpeg, png, webp)

**Respuesta**:
```json
{
  "url": "https://storage.supabase.co/.../imagen.jpg",
  "nombre_archivo": "billete_anverso_123.jpg",
  "tamaño": 1024567,
  "mensaje": "Imagen subida correctamente"
}
```

## Validaciones

### Billete
- `pais_id`: Requerido, debe existir en la tabla paises
- `denominacion`: Requerido, máximo 100 caracteres
- `banco_emisor`: Opcional, máximo 255 caracteres
- `medidas`: Opcional, formato sugerido: "XXX x XXX mm"
- `pick`: Opcional, único si se proporciona
- `estado`: Opcional, valores válidos: UNC, AU, XF, VF, F, VG, G, P
- `precio`: Opcional, debe ser >= 0
- `url_anverso`, `url_reverso`: URLs válidas
- `caracteristicas_ids`: Array de IDs válidos de características

### Característica
- `nombre`: Requerido, único, máximo 100 caracteres
- `color`: Formato hex válido (#XXXXXX)
- `descripcion`: Opcional, máximo 500 caracteres

## Códigos de Error

- `400`: Datos inválidos o faltantes
- `401`: No autenticado
- `403`: Sin permisos
- `404`: Recurso no encontrado
- `409`: Conflicto (ej: pick duplicado)
- `413`: Archivo muy grande
- `415`: Tipo de archivo no soportado
- `422`: Error de validación
- `500`: Error interno del servidor

## Índices de Base de Datos Recomendados

```sql
-- Índices para optimizar consultas frecuentes
CREATE INDEX idx_billetes_pais_id ON billetes(pais_id);
CREATE INDEX idx_billetes_vendido ON billetes(vendido);
CREATE INDEX idx_billetes_destacado ON billetes(destacado);
CREATE INDEX idx_billetes_precio ON billetes(precio);
CREATE INDEX idx_billetes_fecha_creacion ON billetes(fecha_creacion);
CREATE INDEX idx_billetes_pick ON billetes(pick);
CREATE INDEX idx_billetes_denominacion ON billetes(denominacion);

CREATE INDEX idx_billete_caracteristicas_billete_id ON billete_caracteristicas(billete_id);
CREATE INDEX idx_billete_caracteristicas_caracteristica_id ON billete_caracteristicas(caracteristica_id);

-- Índice de texto completo para búsquedas
CREATE INDEX idx_billetes_search ON billetes USING gin(to_tsvector('spanish', denominacion || ' ' || coalesce(descripcion, '') || ' ' || coalesce(pick, '')));
```

## Consideraciones de Rendimiento

1. **Paginación**: Implementar paginación por cursor para mejor rendimiento en datasets grandes
2. **Cache**: Implementar cache en Redis para consultas frecuentes de estadísticas
3. **Imágenes**: Usar CDN para servir imágenes optimizadas
4. **Búsqueda**: Considerar Elasticsearch para búsquedas complejas en el futuro

## Migraciones

### Migración desde estructura actual

```sql
-- 1. Agregar nuevos campos a tabla billetes
ALTER TABLE billetes 
ADD COLUMN banco_emisor VARCHAR(255),
ADD COLUMN medidas VARCHAR(50),
ADD COLUMN descripcion_anverso TEXT,
ADD COLUMN descripcion_reverso TEXT,
ADD COLUMN url_anverso TEXT,
ADD COLUMN url_reverso TEXT,
ADD COLUMN pick VARCHAR(50),
ADD COLUMN estado VARCHAR(20),
ADD COLUMN vendido BOOLEAN DEFAULT FALSE,
ADD COLUMN destacado BOOLEAN DEFAULT FALSE,
ADD COLUMN fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- 2. Crear tablas nuevas
-- (Ver scripts CREATE TABLE arriba)

-- 3. Migrar datos existentes
UPDATE billetes SET 
    url_anverso = anverso,
    url_reverso = reverso
WHERE anverso IS NOT NULL OR reverso IS NOT NULL;

-- 4. Eliminar campos antiguos después de verificar
-- ALTER TABLE billetes DROP COLUMN anverso, DROP COLUMN reverso;
```

## Testing

### Casos de Prueba Esenciales

1. **CRUD Completo**: Crear, leer, actualizar, eliminar billetes
2. **Filtros**: Verificar todos los filtros de búsqueda
3. **Paginación**: Correcta implementación de límites y offsets
4. **Validaciones**: Todos los campos requeridos y formatos
5. **Relaciones**: Correcta gestión de características
6. **Estados**: Toggle de vendido/destacado
7. **Imágenes**: Subida, validación de formato y tamaño
8. **Rendimiento**: Consultas con datasets grandes

## Seguridad

1. **Autenticación**: JWT tokens para todas las operaciones
2. **Autorización**: Solo administradores pueden modificar billetes
3. **Validación**: Sanitizar todas las entradas
4. **Rate Limiting**: Limitar requests por usuario/IP
5. **CORS**: Configurar correctamente para el frontend
6. **SQL Injection**: Usar prepared statements
7. **XSS**: Escapar outputs HTML

## Monitoreo y Logs

1. **Métricas**: Tiempo de respuesta, errores, uso de memoria
2. **Logs**: Todas las operaciones CRUD con usuario y timestamp
3. **Alertas**: Errores 5xx, tiempo de respuesta alto
4. **Auditoría**: Registro de cambios importantes en billetes

## Implementación FastAPI Recomendada

### Estructura de Archivos
```
backend/
├── app/
│   ├── models/
│   │   ├── billete.py
│   │   ├── caracteristica.py
│   │   └── billete_caracteristica.py
│   ├── schemas/
│   │   ├── billete_schemas.py
│   │   └── caracteristica_schemas.py
│   ├── routers/
│   │   ├── billetes.py
│   │   ├── caracteristicas.py
│   │   └── upload.py
│   ├── services/
│   │   ├── billete_service.py
│   │   └── upload_service.py
│   └── main.py
```

### Ejemplo de Schema Pydantic

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BilleteBase(BaseModel):
    pais_id: int
    banco_emisor: Optional[str] = None
    denominacion: str = Field(..., max_length=100)
    medidas: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    descripcion_anverso: Optional[str] = None
    descripcion_reverso: Optional[str] = None
    url_anverso: Optional[str] = None
    url_reverso: Optional[str] = None
    pick: Optional[str] = Field(None, max_length=50)
    estado: Optional[str] = Field(None, regex="^(UNC|AU|XF|VF|F|VG|G|P)$")
    precio: Optional[float] = Field(None, ge=0)
    vendido: bool = False
    destacado: bool = False

class BilleteCreate(BilleteBase):
    caracteristicas_ids: Optional[List[int]] = []

class BilleteUpdate(BaseModel):
    pais_id: Optional[int] = None
    banco_emisor: Optional[str] = None
    denominacion: Optional[str] = Field(None, max_length=100)
    # ... resto de campos opcionales

class BilleteResponse(BilleteBase):
    id: int
    caracteristicas: List[dict] = []
    pais: dict = {}
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
```

Este documento debe actualizarse conforme se implementen nuevas funcionalidades o se modifiquen los requisitos.