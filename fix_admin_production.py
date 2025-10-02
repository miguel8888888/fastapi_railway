#!/usr/bin/env python3
"""
Script para regenerar el usuario admin en producción
Ejecutar desde Render Web Service o localmente contra la BD de producción
"""

import sys
import os
from sqlalchemy.orm import Session

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.usuarios import Usuario, UserRole
from app.utils.security import hash_password

def fix_admin_user():
    """Regenera el hash del usuario administrador"""
    
    # Crear todas las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        print("🔧 Regenerando usuario administrador...")
        
        # Buscar el usuario admin
        admin_user = db.query(Usuario).filter(Usuario.email == "admin@numismatica.com").first()
        
        if not admin_user:
            # Si no existe, crearlo
            print("👤 Creando usuario administrador...")
            admin_user = Usuario(
                email="admin@numismatica.com",
                password_hash=hash_password("admin123"),
                nombre="Administrador",
                apellidos="Sistema",
                role=UserRole.super_admin,
                activo=True
            )
            db.add(admin_user)
        else:
            # Si existe, solo actualizar el hash
            print("🔄 Actualizando hash de contraseña...")
            admin_user.password_hash = hash_password("admin123")
        
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Usuario administrador regenerado exitosamente!")
        print("=" * 50)
        print(f"📧 Email: {admin_user.email}")
        print(f"👤 Nombre: {admin_user.nombre} {admin_user.apellidos}")
        print(f"🛡️ Rol: {admin_user.role.value}")
        print(f"🔐 Contraseña: admin123")
        print("=" * 50)
        
        # Verificar que el hash funciona
        from app.utils.security import verify_password
        if verify_password("admin123", admin_user.password_hash):
            print("✅ Verificación de contraseña exitosa")
        else:
            print("❌ Error: La verificación de contraseña falló")
        
    except Exception as e:
        print(f"❌ Error al regenerar el usuario administrador: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_admin_user()