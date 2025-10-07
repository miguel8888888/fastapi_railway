#!/usr/bin/env python3
"""
Script para mantener actualizada la documentación de API
Ejecutar después de cada cambio en endpoints
"""

import json
from datetime import datetime
from pathlib import Path

# Configuración
API_DOC_FILE = "API_MASTER_REFERENCE.md"
VERSION_FILE = "api_version.json"

def update_version_info():
    """Actualizar información de versión y fecha"""
    version_info = {
        "version": "1.2.0",
        "last_updated": datetime.now().strftime("%d de %B de %Y"),
        "endpoints_count": count_endpoints(),
        "changelog": []
    }
    
    # Guardar información de versión
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(version_info, f, indent=2, ensure_ascii=False)
    
    return version_info

def count_endpoints():
    """Contar endpoints disponibles leyendo el archivo de documentación"""
    if not Path(API_DOC_FILE).exists():
        return 0
    
    with open(API_DOC_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Contar líneas que contienen endpoints (formato | `/endpoint` | METHOD |)
    endpoint_lines = [line for line in content.split('\n') 
                     if line.strip().startswith('| `/') and '|' in line]
    
    return len(endpoint_lines)

def add_changelog_entry(version, description, changes):
    """Agregar entrada al changelog"""
    changelog_entry = f"""
### **v{version} - {datetime.now().strftime('%d de %B de %Y')}**
{description}
{chr(10).join(f'- ✅ {change}' for change in changes)}
"""
    
    # Leer archivo actual
    if Path(API_DOC_FILE).exists():
        with open(API_DOC_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar la sección de changelog e insertar la nueva entrada
        changelog_marker = "## 📝 **CHANGELOG**"
        if changelog_marker in content:
            parts = content.split(changelog_marker)
            if len(parts) >= 2:
                # Insertar después del marcador
                existing_changelog = parts[1]
                new_content = parts[0] + changelog_marker + changelog_entry + existing_changelog
                
                with open(API_DOC_FILE, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Changelog actualizado con versión v{version}")
                return True
    
    print("❌ No se pudo actualizar el changelog")
    return False

def update_last_modified_date():
    """Actualizar la fecha de última modificación en el documento"""
    if not Path(API_DOC_FILE).exists():
        print(f"❌ Archivo {API_DOC_FILE} no encontrado")
        return False
    
    with open(API_DOC_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y reemplazar la línea de fecha
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('**Última Actualización:**'):
            lines[i] = f'**Última Actualización:** {datetime.now().strftime("%d de %B de %Y")}'
            break
    
    # Guardar archivo actualizado
    with open(API_DOC_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Fecha actualizada en {API_DOC_FILE}")
    return True

def main():
    """Función principal"""
    print("🔄 Actualizando documentación de API...")
    
    # Actualizar fecha de modificación
    update_last_modified_date()
    
    # Actualizar información de versión
    version_info = update_version_info()
    print(f"✅ Versión actual: v{version_info['version']}")
    print(f"📊 Total de endpoints: {version_info['endpoints_count']}")
    print(f"📅 Última actualización: {version_info['last_updated']}")

if __name__ == "__main__":
    main()

# Funciones auxiliares para uso manual
def add_new_endpoint(method, endpoint, description, auth_required=False):
    """
    Función helper para documentar un nuevo endpoint
    
    Ejemplo de uso:
    add_new_endpoint("POST", "/billetes/upload", "Subir imagen de billete", True)
    """
    print(f"📝 Nuevo endpoint documentado:")
    print(f"   {method} {endpoint}")
    print(f"   Descripción: {description}")
    print(f"   Autenticación: {'✅ Requerida' if auth_required else '❌ No requerida'}")
    print(f"   💡 Recuerda actualizar manualmente la tabla de endpoints en {API_DOC_FILE}")

def add_version_bump(new_version, changes_list):
    """
    Función helper para documentar una nueva versión
    
    Ejemplo de uso:
    add_version_bump("1.3.0", [
        "Agregado endpoint de upload de imágenes",
        "Mejorado sistema de filtros",
        "Optimización de base de datos"
    ])
    """
    description = f"**Nueva versión con {len(changes_list)} mejoras implementadas**"
    add_changelog_entry(new_version, description, changes_list)
    
    # Actualizar versión en el archivo
    if Path(API_DOC_FILE).exists():
        with open(API_DOC_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar versión
        content = content.replace('**Versión API:** 1.2.0', f'**Versión API:** {new_version}')
        
        with open(API_DOC_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Versión bumped a v{new_version}")

# Ejemplos de uso comentados:
"""
# Para agregar un nuevo endpoint:
add_new_endpoint("POST", "/billetes/{id}/upload", "Subir imagen", True)

# Para documentar una nueva versión:
add_version_bump("1.3.0", [
    "Agregado sistema de upload de imágenes",
    "Mejorados filtros de búsqueda",
    "Optimización de rendimiento"
])
"""