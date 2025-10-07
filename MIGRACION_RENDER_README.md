# 🚀 Instrucciones de Migración para Render

## 📋 Pasos para Actualizar el Sistema de Billetes en Producción

### 1. ✅ **Código ya Desplegado**
Los cambios se han subido a GitHub y Render debería haberlos detectado automáticamente.

### 2. 🗄️ **Migrar Base de Datos PostgreSQL**

Una vez que el nuevo código esté desplegado en Render, necesitas ejecutar la migración de la base de datos:

#### **Opción A: Desde la Consola Web de Render**
1. Ve a tu servicio en Render Dashboard
2. Abre el **Shell** del servicio
3. Ejecuta el comando:
```bash
python migrate_production.py
```

#### **Opción B: Desde la Terminal Local (si tienes acceso directo)**
1. Conecta a la base de datos de Render usando las credenciales
2. Ejecuta el script de migración

### 3. 🔍 **Verificar que la Migración fue Exitosa**

Después de ejecutar la migración, deberías ver:

```
🚀 INICIANDO MIGRACIÓN DE PRODUCCIÓN
==================================================
🔗 Conectando a base de datos...
✅ Tabla 'caracteristicas' ya existe (o creada)
✅ Tabla 'billete_caracteristicas' ya existe (o creada)
➕ Agregando columnas nuevas...
✅ Columnas agregadas
📋 Insertando características iniciales...
✅ Insertadas 10 características
📋 Creando índices de optimización...
✅ Índices creados
✅ ¡MIGRACIÓN DE PRODUCCIÓN COMPLETADA EXITOSAMENTE!
```

### 4. 🧪 **Probar los Nuevos Endpoints**

Una vez migrada la base de datos, puedes probar los nuevos endpoints:

#### **Endpoints Públicos (sin autenticación):**
- `GET /billetes/` - Listar billetes con filtros
- `GET /billetes/{id}` - Obtener billete específico
- `GET /billetes/destacados` - Obtener destacados
- `GET /billetes/caracteristicas` - Listar características

#### **Endpoints Protegidos (requieren autenticación):**
- `POST /billetes/` - Crear billete
- `PUT /billetes/{id}` - Actualizar billete
- `DELETE /billetes/{id}` - Eliminar billete
- `GET /billetes/estadisticas` - Estadísticas
- CRUD completo de características

### 5. 📊 **Nuevas Funcionalidades Disponibles**

#### **Filtros Avanzados:**
```
GET /billetes/?pais_id=1&precio_min=10&precio_max=100&estado=Bueno&destacado=true&page=1&per_page=20
```

#### **Búsqueda General:**
```
GET /billetes/?search=dolar&page=1&per_page=20
```

#### **Estadísticas:**
```
GET /billetes/estadisticas
```
(Requiere autenticación)

### 6. ⚠️ **Posibles Problemas y Soluciones**

#### **Error: "tabla ya existe"**
- ✅ Normal, indica que la tabla ya estaba creada
- La migración continuará sin problemas

#### **Error: "columna ya existe"**
- ✅ Normal, indica que las columnas ya fueron agregadas
- No se perderán datos

#### **Error de conexión a la base de datos**
- Verificar que `DATABASE_URL` esté configurada en Render
- Verificar que el servicio PostgreSQL esté funcionando

### 7. 🎯 **Verificación Final**

Para verificar que todo funciona:

1. **Visita la documentación:** `https://tu-app.onrender.com/docs`
2. **Prueba un endpoint:** `https://tu-app.onrender.com/billetes/caracteristicas`
3. **Verifica las características:** Deberías ver 10 características predefinidas

### 8. 🔄 **Si Algo Sale Mal**

Si hay algún problema con la migración:

1. **Rollback seguro:** La migración está diseñada para no perder datos
2. **Re-ejecutar:** Puedes ejecutar `python migrate_production.py` múltiples veces sin problemas
3. **Logs detallados:** Revisa los logs para identificar el problema exacto

---

## 🎉 ¡Sistema de Billetes Listo!

Una vez completada la migración, tendrás:
- ✅ 11 nuevos campos en la tabla billetes
- ✅ Sistema completo de características con colores
- ✅ Filtros avanzados y paginación
- ✅ Estadísticas detalladas
- ✅ 11 nuevos endpoints API
- ✅ Base de datos completamente migrada

**¡Tu sistema de billetes está listo para usar en producción!** 🚀