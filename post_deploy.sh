#!/bin/bash

# Script de post-deployment para Render
# Este script se ejecuta después del despliegue para migrar la base de datos

echo "🚀 Ejecutando migraciones post-deployment..."

# Ejecutar la migración de producción
python migrate_production.py

if [ $? -eq 0 ]; then
    echo "✅ Migraciones completadas exitosamente"
else
    echo "❌ Error en las migraciones"
    exit 1
fi

echo "🎯 Sistema de billetes listo en producción"