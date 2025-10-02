#!/usr/bin/env python3
"""
Script para actualizar el email del usuario administrador
"""

import sys
import os
from sqlalchemy.orm import Session

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models.usuarios import Usuario
from app.utils.security import hash_password

def update_admin_email():
    """Actualiza el email del usuario administrador"""
    
    db: Session = SessionLocal()
    
    try:
        print("🔧 ACTUALIZANDO EMAIL DEL ADMINISTRADOR")
        print("=" * 45)
        
        # Buscar usuario administrador actual
        admin_user = db.query(Usuario).filter(
            Usuario.email == "admin@numismatica.com"
        ).first()
        
        if not admin_user:
            print("❌ No se encontró usuario administrador con email admin@numismatica.com")
            
            # Buscar cualquier usuario admin
            admin_user = db.query(Usuario).filter(
                Usuario.role.in_(["admin", "super_admin"])
            ).first()
            
            if admin_user:
                print(f"📧 Se encontró admin con email: {admin_user.email}")
            else:
                print("❌ No se encontró ningún usuario administrador")
                return False
        
        # Mostrar información actual
        print(f"👤 Usuario encontrado:")
        print(f"   Email actual: {admin_user.email}")
        print(f"   Nombre: {admin_user.nombre} {admin_user.apellidos or ''}")
        print(f"   Rol: {admin_user.role}")
        
        # Verificar si ya tiene el email correcto
        if admin_user.email == "miguelsgap@gmail.com":
            print("✅ El usuario ya tiene el email correcto: miguelsgap@gmail.com")
            return True
        
        # Verificar si ya existe otro usuario con ese email
        existing_user = db.query(Usuario).filter(
            Usuario.email == "miguelsgap@gmail.com"
        ).first()
        
        if existing_user and existing_user.id != admin_user.id:
            print(f"⚠️ Ya existe otro usuario con email miguelsgap@gmail.com")
            print(f"   ID: {existing_user.id}, Nombre: {existing_user.nombre}")
            print("   Actualizando ese usuario como admin...")
            
            # Hacer que el usuario existente sea admin
            existing_user.role = admin_user.role
            existing_user.activo = True
            
            # Opcional: eliminar el admin anterior o cambiar su email
            admin_user.email = f"old_admin_{admin_user.id}@numismatica.com"
            admin_user.activo = False
            
            db.commit()
            
            print("✅ Usuario miguelsgap@gmail.com actualizado como administrador")
            print(f"📧 Nuevo email admin: miguelsgap@gmail.com")
            return True
        
        # Actualizar email del admin actual
        old_email = admin_user.email
        admin_user.email = "miguelsgap@gmail.com"
        
        db.commit()
        
        print("🎉 EMAIL ACTUALIZADO EXITOSAMENTE!")
        print("=" * 40)
        print(f"📧 Email anterior: {old_email}")
        print(f"📧 Email nuevo: miguelsgap@gmail.com")
        print(f"👤 Nombre: {admin_user.nombre} {admin_user.apellidos or ''}")
        print(f"🛡️ Rol: {admin_user.role}")
        print("=" * 40)
        print("✅ Ahora puedes usar miguelsgap@gmail.com para:")
        print("   - Login como administrador")
        print("   - Recuperación de contraseña")
        print("   - Recibir emails del sistema")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar email: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def show_admin_info():
    """Muestra información de todos los usuarios admin"""
    
    db: Session = SessionLocal()
    
    try:
        print("\n📋 USUARIOS ADMINISTRADORES EN EL SISTEMA:")
        print("=" * 50)
        
        admin_users = db.query(Usuario).filter(
            Usuario.role.in_(["admin", "super_admin"])
        ).all()
        
        if not admin_users:
            print("❌ No se encontraron usuarios administradores")
            return
        
        for i, admin in enumerate(admin_users, 1):
            status = "✅ Activo" if admin.activo else "❌ Inactivo"
            print(f"{i}. {admin.nombre} {admin.apellidos or ''}")
            print(f"   📧 Email: {admin.email}")
            print(f"   🛡️ Rol: {admin.role}")
            print(f"   📊 Estado: {status}")
            print(f"   🆔 ID: {admin.id}")
            print("   ---")
            
    except Exception as e:
        print(f"❌ Error al consultar usuarios: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    show_admin_info()
    print()
    update_admin_email()
    print()
    show_admin_info()