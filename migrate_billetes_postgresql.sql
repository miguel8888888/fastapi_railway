-- Script SQL directo para agregar columnas faltantes a la tabla billetes en PostgreSQL
-- Ejecutar directamente en la consola de PostgreSQL de Render

-- 1. Verificar columnas actuales (opcional)
-- SELECT column_name FROM information_schema.columns WHERE table_name = 'billetes';

-- 2. Agregar columnas nuevas una por una
-- IMPORTANTE: Usar IF NOT EXISTS para evitar errores si ya existen

-- Agregar banco_emisor
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'banco_emisor') THEN
        ALTER TABLE billetes ADD COLUMN banco_emisor VARCHAR(255);
        RAISE NOTICE 'Columna banco_emisor agregada';
    ELSE
        RAISE NOTICE 'Columna banco_emisor ya existe';
    END IF;
END $$;

-- Agregar medidas
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'medidas') THEN
        ALTER TABLE billetes ADD COLUMN medidas VARCHAR(50);
        RAISE NOTICE 'Columna medidas agregada';
    ELSE
        RAISE NOTICE 'Columna medidas ya existe';
    END IF;
END $$;

-- Agregar descripcion_anverso
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'descripcion_anverso') THEN
        ALTER TABLE billetes ADD COLUMN descripcion_anverso TEXT;
        RAISE NOTICE 'Columna descripcion_anverso agregada';
    ELSE
        RAISE NOTICE 'Columna descripcion_anverso ya existe';
    END IF;
END $$;

-- Agregar descripcion_reverso
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'descripcion_reverso') THEN
        ALTER TABLE billetes ADD COLUMN descripcion_reverso TEXT;
        RAISE NOTICE 'Columna descripcion_reverso agregada';
    ELSE
        RAISE NOTICE 'Columna descripcion_reverso ya existe';
    END IF;
END $$;

-- Agregar url_anverso
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'url_anverso') THEN
        ALTER TABLE billetes ADD COLUMN url_anverso TEXT;
        RAISE NOTICE 'Columna url_anverso agregada';
    ELSE
        RAISE NOTICE 'Columna url_anverso ya existe';
    END IF;
END $$;

-- Agregar url_reverso
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'url_reverso') THEN
        ALTER TABLE billetes ADD COLUMN url_reverso TEXT;
        RAISE NOTICE 'Columna url_reverso agregada';
    ELSE
        RAISE NOTICE 'Columna url_reverso ya existe';
    END IF;
END $$;

-- Agregar pick
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'pick') THEN
        ALTER TABLE billetes ADD COLUMN pick VARCHAR(50);
        RAISE NOTICE 'Columna pick agregada';
    ELSE
        RAISE NOTICE 'Columna pick ya existe';
    END IF;
END $$;

-- Agregar estado
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'estado') THEN
        ALTER TABLE billetes ADD COLUMN estado VARCHAR(20) DEFAULT 'Bueno';
        RAISE NOTICE 'Columna estado agregada';
    ELSE
        RAISE NOTICE 'Columna estado ya existe';
    END IF;
END $$;

-- Agregar vendido
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'vendido') THEN
        ALTER TABLE billetes ADD COLUMN vendido BOOLEAN DEFAULT false;
        RAISE NOTICE 'Columna vendido agregada';
    ELSE
        RAISE NOTICE 'Columna vendido ya existe';
    END IF;
END $$;

-- Agregar destacado
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'destacado') THEN
        ALTER TABLE billetes ADD COLUMN destacado BOOLEAN DEFAULT false;
        RAISE NOTICE 'Columna destacado agregada';
    ELSE
        RAISE NOTICE 'Columna destacado ya existe';
    END IF;
END $$;

-- Agregar fecha_actualizacion
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'billetes' AND column_name = 'fecha_actualizacion') THEN
        ALTER TABLE billetes ADD COLUMN fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;
        RAISE NOTICE 'Columna fecha_actualizacion agregada';
    ELSE
        RAISE NOTICE 'Columna fecha_actualizacion ya existe';
    END IF;
END $$;

-- 3. Migrar URLs de imágenes existentes
UPDATE billetes 
SET url_anverso = anverso, 
    url_reverso = reverso 
WHERE url_anverso IS NULL AND anverso IS NOT NULL;

-- 4. Crear índices para optimización
CREATE INDEX IF NOT EXISTS idx_billetes_pais ON billetes(pais);
CREATE INDEX IF NOT EXISTS idx_billetes_vendido ON billetes(vendido);
CREATE INDEX IF NOT EXISTS idx_billetes_destacado ON billetes(destacado);
CREATE INDEX IF NOT EXISTS idx_billetes_denominacion ON billetes(denominacion);
CREATE INDEX IF NOT EXISTS idx_billetes_pick ON billetes(pick);

-- 5. Verificar resultado final
SELECT 
    'Migración completada. Total columnas en billetes:' as mensaje,
    COUNT(*) as total_columnas
FROM information_schema.columns 
WHERE table_name = 'billetes';

-- Mostrar todas las columnas
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'billetes' 
ORDER BY ordinal_position;