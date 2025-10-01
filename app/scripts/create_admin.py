#!/usr/bin/env python3
"""
Script para crear usuario administrador por defecto
Ejecutar: python -m app.scripts.create_admin
"""

import sys
import os
from sqlalchemy.orm import Session

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal, engine, Base
from app.models.usuarios import Usuario, UserRole
from app.utils.security import hash_password

def create_default_admin():
    """Crea el usuario administrador por defecto si no existe"""
    
    # Crear todas las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Verificar si ya existe un admin
        existing_admin = db.query(Usuario).filter(Usuario.email == "admin@numismatica.com").first()
        
        if existing_admin:
            print("✅ El usuario administrador ya existe.")
            print(f"   Email: {existing_admin.email}")
            print(f"   Nombre: {existing_admin.nombre}")
            print(f"   Rol: {existing_admin.role.value}")
            return
        
        # Crear usuario administrador
        admin_user = Usuario(
            email="admin@numismatica.com",
            password_hash=hash_password("admin123"),
            nombre="Administrador",
            apellidos="Sistema",
            role=UserRole.super_admin,
            activo=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("🎉 Usuario administrador creado exitosamente!")
        print("=" * 50)
        print(f"📧 Email: admin@numismatica.com")
        print(f"🔐 Contraseña: admin123")
        print(f"👤 Nombre: {admin_user.nombre} {admin_user.apellidos}")
        print(f"🛡️ Rol: {admin_user.role.value}")
        print("=" * 50)
        print("⚠️  IMPORTANTE: Cambia esta contraseña después del primer login!")
        
    except Exception as e:
        print(f"❌ Error al crear el usuario administrador: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_default_admin()