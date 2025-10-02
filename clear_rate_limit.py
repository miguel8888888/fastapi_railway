#!/usr/bin/env python3
"""
Script para limpiar rate limiting y intentos de login fallidos
Ejecutar en Render Shell o localmente contra la BD de producción
"""

import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.usuarios import Usuario
from app.models.auth import LoginAttempt

def clear_rate_limiting():
    """Limpia todos los intentos de login y desbloquea usuarios"""
    
    db: Session = SessionLocal()
    
    try:
        print("🧹 Limpiando rate limiting y intentos fallidos...")
        
        # Limpiar todos los intentos de login
        attempts_deleted = db.query(LoginAttempt).delete()
        print(f"   🗑️ {attempts_deleted} intentos de login eliminados")
        
        # Desbloquear todos los usuarios
        blocked_users = db.query(Usuario).filter(Usuario.bloqueado_hasta.isnot(None)).all()
        
        for user in blocked_users:
            print(f"   🔓 Desbloqueando usuario: {user.email}")
            user.bloqueado_hasta = None
            user.intentos_fallidos = 0
        
        # Resetear contador de intentos fallidos
        db.query(Usuario).update({
            Usuario.intentos_fallidos: 0,
            Usuario.bloqueado_hasta: None
        })
        
        db.commit()
        
        print("✅ Rate limiting limpiado exitosamente!")
        print("=" * 50)
        print("🚀 Ahora puedes intentar login nuevamente")
        print("📧 Email: admin@numismatica.com")  
        print("🔐 Password: admin123")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error al limpiar rate limiting: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_rate_limiting()