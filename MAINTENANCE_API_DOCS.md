# 📝 GUÍA DE MANTENIMIENTO - DOCUMENTACIÓN API

## 🎯 **OBJETIVO**

Este documento explica cómo mantener actualizada la documentación de API (`API_MASTER_REFERENCE.md`) cada vez que se realizan cambios en el sistema.

---

## 📋 **ARCHIVOS DE DOCUMENTACIÓN**

### **Archivo Principal:**
- `API_MASTER_REFERENCE.md` - **Documentación maestra de todas las APIs**

### **Archivos de Soporte:**
- `update_api_docs.py` - Script para actualizar fechas y versiones
- `api_version.json` - Configuración de versión y changelog
- `MAINTENANCE_API_DOCS.md` - Esta guía (este archivo)

---

## 🔄 **PROCESO DE ACTUALIZACIÓN**

### **1️⃣ Cuando agregues un NUEVO ENDPOINT:**

1. **Actualizar la tabla de índice** en `API_MASTER_REFERENCE.md`:
```markdown
| `/nuevo-endpoint` | POST | ✅ Sí | Descripción del endpoint |
```

2. **Agregar la documentación completa** en la sección correspondiente:
```markdown
### **➕ Nuevo Endpoint**
```http
POST /nuevo-endpoint
Authorization: Bearer {token}
```

**Cuerpo:**
```json
{
  "campo": "valor"
}
```

**Respuesta 201:**
```json
{
  "id": 1,
  "campo": "valor"
}
```
```

3. **Ejecutar el script de actualización:**
```bash
python update_api_docs.py
```

---

### **2️⃣ Cuando MODIFIQUES un endpoint existente:**

1. **Actualizar la documentación** del endpoint afectado
2. **Cambiar ejemplos de JSON** si la estructura cambió
3. **Actualizar códigos de error** si se agregaron nuevos
4. **Ejecutar script de actualización**

---

### **3️⃣ Cuando ELIMINES un endpoint:**

1. **Remover de la tabla de índice**
2. **Eliminar toda la documentación** de ese endpoint
3. **Actualizar el contador** en `api_version.json`
4. **Documentar en el changelog** como "breaking change"

---

## 🚀 **SCRIPTS AUTOMÁTICOS**

### **Actualización de Fecha:**
```bash
python update_api_docs.py
```
- ✅ Actualiza "Última Actualización" 
- ✅ Cuenta endpoints automáticamente
- ✅ Actualiza `api_version.json`

### **Bump de Versión:**
```python
# En update_api_docs.py
add_version_bump("1.3.0", [
    "Agregado sistema de upload",
    "Mejorados filtros avanzados",
    "Fix en autenticación"
])
```

### **Nuevo Endpoint:**
```python
# En update_api_docs.py
add_new_endpoint("POST", "/billetes/upload", "Subir imagen", True)
```

---

## 📊 **VERSIONADO**

### **Semantic Versioning:**
- `1.X.0` - Cambios mayores (nuevas funcionalidades)
- `1.2.X` - Cambios menores (bug fixes, optimizaciones)

### **Cuando incrementar versión:**

#### **MAJOR (1.X.0):**
- Nuevos endpoints importantes
- Cambios en estructura de respuestas
- Breaking changes

#### **MINOR (1.2.X):**
- Bug fixes
- Optimizaciones
- Pequeñas mejoras

---

## ✅ **CHECKLIST DE ACTUALIZACIÓN**

Cada vez que modifiques las APIs, verifica:

### **📋 Documentación Básica:**
- [ ] Tabla de índice actualizada
- [ ] Método HTTP correcto
- [ ] URL del endpoint correcta
- [ ] Indicador de autenticación correcto
- [ ] Descripción clara

### **📋 Documentación Detallada:**
- [ ] Parámetros de URL documentados
- [ ] Query parameters documentados
- [ ] Cuerpo de petición documentado
- [ ] Headers requeridos documentados
- [ ] Respuesta exitosa documentada
- [ ] Códigos de error documentados

### **📋 Ejemplos:**
- [ ] JSON de request actualizado
- [ ] JSON de response actualizado
- [ ] Ejemplos realistas
- [ ] Todos los campos incluidos

### **📋 Metadatos:**
- [ ] Fecha actualizada
- [ ] Versión incrementada si corresponde
- [ ] Changelog actualizado
- [ ] Contador de endpoints correcto

---

## 🔧 **HERRAMIENTAS ÚTILES**

### **Validar JSON:**
```bash
# Para validar que los ejemplos JSON son válidos
python -m json.tool ejemplo.json
```

### **Contar Endpoints:**
```bash
# Contar líneas que contienen endpoints en la documentación
grep -c "| \`/" API_MASTER_REFERENCE.md
```

### **Ver Cambios:**
```bash
# Ver diferencias desde el último commit
git diff HEAD~1 API_MASTER_REFERENCE.md
```

---

## 📚 **RECURSOS ADICIONALES**

### **Documentación Automática:**
- Swagger UI: `/docs` - Siempre actualizada automáticamente
- ReDoc: `/redoc` - Generada desde el código

### **Testing:**
- Probar cada endpoint documentado
- Verificar que los ejemplos funcionan
- Validar códigos de error

---

## 🚨 **ERRORES COMUNES**

### **❌ No actualizar tabla de índice**
- Endpoint documentado pero no aparece en la tabla
- **Fix:** Agregar línea en la tabla de índice

### **❌ JSON inválido en ejemplos**
- Ejemplos con sintaxis JSON incorrecta
- **Fix:** Validar con `python -m json.tool`

### **❌ Códigos de respuesta incorrectos**
- Documentar 200 cuando devuelve 201
- **Fix:** Probar endpoint y verificar código real

### **❌ Parámetros faltantes**
- No documentar todos los parámetros disponibles
- **Fix:** Revisar el código del endpoint

---

## 🎯 **RESPONSABILIDADES**

### **Desarrollador Backend:**
- ✅ Actualizar documentación al agregar/modificar endpoints
- ✅ Ejecutar script de actualización
- ✅ Probar que ejemplos funcionen
- ✅ Incrementar versión cuando corresponda

### **Frontend/Usuario de API:**
- ✅ Reportar discrepancias entre documentación y API real
- ✅ Solicitar clarificaciones en ejemplos
- ✅ Sugerir mejoras en la documentación

---

## 📞 **CONTACTO**

Si encuentras problemas con la documentación o necesitas agregar nuevas secciones, crear un issue en el repositorio con la etiqueta `documentation`.

---

**🔄 Mantener esta documentación actualizada es responsabilidad de todo el equipo**