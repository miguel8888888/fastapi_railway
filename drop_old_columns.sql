-- =====================================================
-- SCRIPT PARA ELIMINAR COLUMNAS anverso Y reverso
-- Ejecutar en PgAdmin después de verificar migración
-- =====================================================

-- 1. Verificar que las nuevas columnas tienen datos
SELECT 
    COUNT(*) as total_billetes,
    COUNT(url_anverso) as con_url_anverso,
    COUNT(url_reverso) as con_url_reverso,
    COUNT(anverso) as con_anverso_viejo,
    COUNT(reverso) as con_reverso_viejo
FROM billetes;

-- 2. Ver algunos ejemplos antes de eliminar (opcional)
SELECT 
    id, 
    anverso, 
    reverso, 
    url_anverso, 
    url_reverso 
FROM billetes 
WHERE anverso IS NOT NULL OR reverso IS NOT NULL
LIMIT 3;

-- 3. ELIMINAR LAS COLUMNAS OBSOLETAS
ALTER TABLE billetes DROP COLUMN IF EXISTS anverso;
ALTER TABLE billetes DROP COLUMN IF EXISTS reverso;

-- 4. Verificar el resultado final
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'billetes' 
ORDER BY ordinal_position;

-- 5. Contar columnas finales
SELECT COUNT(*) as total_columnas_finales
FROM information_schema.columns 
WHERE table_name = 'billetes';