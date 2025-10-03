# Gestión de Imágenes de Perfil con Supabase

## Descripción
Esta funcionalidad permite a los usuarios subir y gestionar imágenes de perfil utilizando Supabase como servicio de almacenamiento. Se almacenan tanto la URL pública como la ruta interna para facilitar la gestión y eliminación de archivos.

## Nuevos Campos

### En la base de datos (tabla `usuarios`)
- `profile_image` (VARCHAR(500)): URL pública de la imagen desde Supabase
- `profile_image_path` (VARCHAR(300)): Ruta interna del archivo en Supabase para gestión

## Endpoints Actualizados

### PUT /auth/perfil/
Ahora acepta campos opcionales de imagen:

```json
{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "telefono": "+1234567890",
  "ciudad": "Madrid",
  "direccion": "Calle Principal 123",
  "pais": "España",
  "profile_image": "https://your-supabase-url/storage/v1/object/public/img-billetes/user123/profile.jpg",
  "profile_image_path": "user123/profile.jpg"
}
```

## Ejemplos de Uso

### 1. Actualizar perfil con imagen
```bash
curl -X PUT "http://localhost:8000/auth/perfil/" \
-H "Authorization: Bearer tu_jwt_token" \
-H "Content-Type: application/json" \
-d '{
  "nombre": "Juan Actualizado",
  "profile_image": "https://tu-proyecto.supabase.co/storage/v1/object/public/img-billetes/user123/nueva-foto.jpg",
  "profile_image_path": "user123/nueva-foto.jpg"
}'
```

### 2. Solo actualizar imagen de perfil
```bash
curl -X PUT "http://localhost:8000/auth/perfil/" \
-H "Authorization: Bearer tu_jwt_token" \
-H "Content-Type: application/json" \
-d '{
  "profile_image": "https://tu-proyecto.supabase.co/storage/v1/object/public/img-billetes/user123/avatar.jpg",
  "profile_image_path": "user123/avatar.jpg"
}'
```

### 3. Eliminar imagen de perfil
```bash
curl -X PUT "http://localhost:8000/auth/perfil/" \
-H "Authorization: Bearer tu_jwt_token" \
-H "Content-Type: application/json" \
-d '{
  "profile_image": null,
  "profile_image_path": null
}'
```

## Flujo Recomendado en Frontend

### 1. Subida de imagen a Supabase
```javascript
// Frontend: Subir imagen a Supabase
const supabase = createClient(supabaseUrl, supabaseKey);

async function uploadProfileImage(file, userId) {
  const fileName = `${userId}/profile-${Date.now()}.${file.name.split('.').pop()}`;
  const filePath = fileName;

  const { data, error } = await supabase.storage
    .from('img-billetes')
    .upload(filePath, file);

  if (error) throw error;

  // Obtener URL pública
  const { data: publicURL } = supabase.storage
    .from('img-billetes')
    .getPublicUrl(filePath);

  return {
    profile_image: publicURL.publicUrl,
    profile_image_path: filePath
  };
}
```

### 2. Actualizar perfil en API
```javascript
// Actualizar perfil con nueva imagen
async function updateProfileWithImage(imageData) {
  const response = await fetch('/auth/perfil/', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(imageData)
  });

  return response.json();
}
```

### 3. Eliminar imagen anterior de Supabase
```javascript
// Si hay una imagen anterior, eliminarla de Supabase
async function deleteOldProfileImage(oldImagePath) {
  if (oldImagePath) {
    const { error } = await supabase.storage
      .from('img-billetes')
      .remove([oldImagePath]);
    
    if (error) console.error('Error eliminando imagen anterior:', error);
  }
}
```

## Respuesta del Endpoint

### Exitosa (200)
```json
{
  "message": "Perfil actualizado exitosamente",
  "user": {
    "id": "uuid-del-usuario",
    "email": "usuario@ejemplo.com",
    "nombre": "Juan Pérez",
    "telefono": "+1234567890",
    "ciudad": "Madrid",
    "direccion": "Calle Principal 123",
    "pais": "España",
    "profile_image": "https://tu-proyecto.supabase.co/storage/v1/object/public/img-billetes/user123/profile.jpg",
    "profile_image_path": "user123/profile.jpg",
    "es_administrador": false,
    "fecha_creacion": "2024-01-01T00:00:00"
  }
}
```

### Error - Email duplicado (400)
```json
{
  "detail": "Ya existe un usuario con este email"
}
```

## Consideraciones de Seguridad

1. **Validación de URLs**: Las URLs de Supabase deben validarse para asegurar que pertenecen a tu proyecto
2. **Tamaño de archivos**: Implementar límites de tamaño en el frontend y Supabase
3. **Tipos de archivo**: Solo permitir formatos de imagen válidos (jpg, png, webp, etc.)
4. **Limpieza**: Eliminar imágenes anteriores cuando se actualice el perfil

## Configuración de Supabase

### 1. Crear bucket para imágenes
```sql
-- En Supabase SQL Editor
insert into storage.buckets (id, name, public)
values ('img-billetes', 'img-billetes', true);
```

### 2. Política de seguridad para subida
```sql
-- Permitir a usuarios autenticados subir sus propias imágenes
create policy "Users can upload own profile image" on storage.objects for insert with check (
  bucket_id = 'img-billetes' and 
  auth.uid()::text = (storage.foldername(name))[1]
);
```

### 3. Política para eliminar imágenes
```sql
-- Permitir a usuarios eliminar sus propias imágenes
create policy "Users can delete own profile image" on storage.objects for delete using (
  bucket_id = 'img-billetes' and 
  auth.uid()::text = (storage.foldername(name))[1]
);
```

## Notas Importantes

- Los campos `profile_image` y `profile_image_path` son opcionales
- Se puede enviar `null` para eliminar la imagen actual
- El campo `profile_image_path` es crucial para eliminar archivos de Supabase
- Recomendado usar nombres únicos para evitar conflictos
- Implementar validación en frontend antes de subir a Supabase