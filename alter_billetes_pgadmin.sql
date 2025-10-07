-- =====================================================
-- SCRIPT PARA PEGAR DIRECTO EN PGADMIN
-- Agrega las 11 columnas faltantes a la tabla billetes
-- =====================================================

-- 1. Verificar columnas actuales (opcional)
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'billetes' 
ORDER BY ordinal_position;

-- 2. Agregar las columnas faltantes una por una
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS banco_emisor VARCHAR(255);
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS medidas VARCHAR(50);
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS descripcion_anverso TEXT;
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS descripcion_reverso TEXT;
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS url_anverso TEXT;
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS url_reverso TEXT;
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS pick VARCHAR(50);
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS estado VARCHAR(20) DEFAULT 'Bueno';
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS vendido BOOLEAN DEFAULT false;
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS destacado BOOLEAN DEFAULT false;
ALTER TABLE billetes ADD COLUMN IF NOT EXISTS fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;

-- 3. Migrar las URLs existentes (si existen datos)
UPDATE billetes 
SET url_anverso = anverso, 
    url_reverso = reverso 
WHERE (url_anverso IS NULL OR url_anverso = '') 
  AND anverso IS NOT NULL 
  AND anverso != '';

-- 4. Crear índices para optimización
CREATE INDEX IF NOT EXISTS idx_billetes_pais ON billetes(pais);
CREATE INDEX IF NOT EXISTS idx_billetes_vendido ON billetes(vendido);
CREATE INDEX IF NOT EXISTS idx_billetes_destacado ON billetes(destacado);
CREATE INDEX IF NOT EXISTS idx_billetes_denominacion ON billetes(denominacion);
CREATE INDEX IF NOT EXISTS idx_billetes_pick ON billetes(pick);

-- 5. Verificar el resultado final
SELECT 
    COUNT(*) as total_columnas,
    string_agg(column_name, ', ' ORDER BY ordinal_position) as columnas
FROM information_schema.columns 
WHERE table_name = 'billetes';

-- 6. Verificar algunos datos de ejemplo
SELECT 
    id, 
    pais, 
    denominacion, 
    banco_emisor, 
    estado, 
    vendido, 
    destacado,
    fecha_actualizacion
FROM billetes 
LIMIT 5;