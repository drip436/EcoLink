"""
create_admin.py
═══════════════════════════════════════════════════════════════════════════════
Script de utilidad para crear el usuario administrador en Supabase.
Ejecutar UNA SOLA VEZ antes de empezar a usar la app:

    python create_admin.py

Luego entra con:
    Email:      admin@ecolink.mx
    Contraseña: admin123
═══════════════════════════════════════════════════════════════════════════════
"""

from sqlmodel import create_engine, Session, select, SQLModel
from ecolink.models.db import User, CollectionRoute, CollectionPoint, Reward
from ecolink.utils.auth import hash_password

DB_URL = (
    "postgresql://postgres.djhiyafzjfwpaqccqdcy:ecolinkinnovatec"
    "@aws-1-us-east-1.pooler.supabase.com:5432/postgres"
)

engine = create_engine(DB_URL, echo=False)


def main():
    print("📦 Creando tablas en Supabase...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas")

    with Session(engine) as db:
        # ── Admin ──────────────────────────────────────────────────────
        existing = db.exec(select(User).where(User.email == "admin@ecolink.mx")).first()
        if not existing:
            admin = User(
                email="admin@ecolink.mx",
                full_name="Administrador EcoLink",
                hashed_password=hash_password("admin123"),
                role="admin",
            )
            db.add(admin)
            db.commit()
            print("👤 Admin creado: admin@ecolink.mx / admin123")
        else:
            print("👤 Admin ya existe")

        # ── Datos de demo (rutas, puntos, recompensas) ─────────────────
        if not db.exec(select(CollectionRoute)).first():
            print("🌱 Insertando datos de demo...")
            for name, waste, zone, status in [
                ("Ruta Norte · Plástico", "plástico", "Centro Norte",    "in_progress"),
                ("Ruta Sur · Orgánico",   "orgánico", "Col. Sur",        "scheduled"),
                ("Ruta Este · Vidrio",    "vidrio",   "Zona Industrial", "scheduled"),
                ("Ruta Oeste · Papel",    "papel",    "Frac. Bello",     "scheduled"),
            ]:
                db.add(CollectionRoute(name=name, waste_type=waste, zone=zone, status=status))

            for nm, addr, lat, lng, types, sch, pts in [
                ("Centro de Acopio Municipal", "Calle 60 #500, Centro",   20.9674, -89.5926, "pilas,aceite,plastico,vidrio,papel", "Lun-Sáb 8:00-17:00", 60),
                ("Punto Verde Altabrisa",      "Av. Altabrisa #200",      21.0012, -89.6145, "pilas,electronico,ropa",             "Lun-Vie 9:00-18:00",  50),
                ("Ecocentro Gran Plaza",       "Gran Plaza, Mérida",      20.9856, -89.6234, "plastico,papel,vidrio",              "Todos los días 10:00-21:00", 40),
                ("Recolección Aceite",         "Calle 21 #301, Col. Méx", 20.9523, -89.5789, "aceite",                             "Mié y Vie 9:00-14:00", 70),
            ]:
                db.add(CollectionPoint(name=nm, address=addr, latitude=lat, longitude=lng,
                                       waste_types=types, schedule=sch, points_per_visit=pts))

            for title, desc, pts, rtype, disc, partner in [
                ("10% desc. en El Giro",        "Descuento en toda la carta.",    100, "discount",    10.0, "Restaurante El Giro"),
                ("Bolsa ecológica reutilizable", "Bolsa de tela con logo EcoLink.",200, "benefit",    None, "Municipio de Mérida"),
                ("Mes gratis transporte",        "Saldo para 30 días de autobús.", 500, "municipal",  None, "TAME Mérida"),
                ("Certificado Ciudadano Eco",    "Reconocimiento oficial.",         800, "certificate",None, "Municipio de Mérida"),
                ("20% en Oxxo Gas",              "Descuento en tu próxima carga.", 300, "discount",   20.0, "Oxxo Gas"),
            ]:
                db.add(Reward(title=title, description=desc, points_required=pts,
                               reward_type=rtype, discount_percent=disc, partner_name=partner))

            db.commit()
            print("✅ Datos de demo insertados")

    print("\n🚀 Todo listo. Ejecuta: reflex run")
    print("   URL: http://localhost:3000")
    print("   Admin: admin@ecolink.mx / admin123")


if __name__ == "__main__":
    main()
