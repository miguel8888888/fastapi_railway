-- =====================================================
-- SQL PARA INSERTAR BILLETE DE 50.000 PESOS COLOMBIANOS
-- Copiar y pegar en PgAdmin
-- =====================================================

-- Insertar el nuevo billete
INSERT INTO billetes (
    pais, 
    denominacion, 
    precio, 
    banco_emisor, 
    medidas,
    descripcion_anverso, 
    descripcion_reverso, 
    url_anverso, 
    url_reverso, 
    pick, 
    estado, 
    vendido, 
    destacado,
    fecha_actualizacion
) VALUES (
    1,                                                                                    -- pais (Colombia)
    '50000',                                                                             -- denominación
    '150000',                                                                            -- precio
    'Banco de la República de Colombia',                                                 -- banco_emisor
    '70 x 140 mm',                                                                      -- medidas
    'Retrato de Gabriel García Márquez, escritor y premio Nobel de Literatura',         -- descripcion_anverso
    'Escenas de Macondo y referencias a sus obras literarias',                         -- descripcion_reverso
    'https://ljmwhelmcwtxbticvuwd.supabase.co/storage/v1/object/public/img-billetes/Reverso%2050%20mil.jpeg',  -- url_anverso
    'https://ljmwhelmcwtxbticvuwd.supabase.co/storage/v1/object/public/img-billetes/Reverso%2050%20mil.jpeg',  -- url_reverso
    'P-458',                                                                            -- pick
    'Excelente',                                                                        -- estado
    false,                                                                              -- vendido
    true,                                                                               -- destacado
    CURRENT_TIMESTAMP                                                                   -- fecha_actualizacion
) RETURNING id, fecha_actualizacion;

-- Verificar que se insertó correctamente
SELECT 
    id,
    pais,
    denominacion,
    precio,
    banco_emisor,
    estado,
    vendido,
    destacado,
    fecha_actualizacion
FROM billetes 
WHERE denominacion = '50000' 
ORDER BY id DESC 
LIMIT 1;