"""
create_admin.py
Ejecutar UNA sola vez desde la raíz del proyecto:
    python create_admin.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlmodel import select
import reflex as rx
from ecolink.models.db import User
from ecolink.utils.auth import hash_password
from dotenv import load_dotenv
load_dotenv()


ADMIN_EMAIL    = os.environ["EMAIL"],
ADMIN_PASSWORD = os.environ["PASSWORD"],
ADMIN_NAME     = os.environ["NAME"],

def create_admin():
    with rx.session() as db:
        existing = db.exec(select(User).where(User.email == ADMIN_EMAIL)).first()
        if existing:
            # Si existe pero no es admin, promoverlo
            if existing.role != "admin":
                existing.role = "admin"
                db.add(existing)
                db.commit()
                print(f"✅ Usuario existente promovido a admin: {ADMIN_EMAIL}")
            else:
                print(f"ℹ️  El admin ya existe: {ADMIN_EMAIL}")
            return

        admin = User(
            email=ADMIN_EMAIL,
            full_name=ADMIN_NAME,
            hashed_password=hash_password(ADMIN_PASSWORD),
            role="admin",
            is_active=True,
            total_points=0,
            level="Semilla",
            recycling_actions=0,
        )
        db.add(admin)
        db.commit()
        print("✅ Cuenta admin creada:")
        print(f"   Email:      {ADMIN_EMAIL}")
        print(f"   Contraseña: {ADMIN_PASSWORD}")
        print(f"   Ruta admin: http://localhost:3000/admin")

if __name__ == "__main__":
    create_admin()