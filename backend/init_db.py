"""
Script para inicializar BD PostgreSQL con datos de demostración
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.route import Route, RouteStatus
from app.models.recycling_point import RecyclingPoint
from app.utils.security import hash_password
from app.config import DATABASE_URL
from datetime import datetime, timedelta
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Inicializar BD PostgreSQL con datos de demostración"""
    logger.info("🗄️ Inicializando base de datos PostgreSQL...")
    logger.info(f"📍 Base de datos: {DATABASE_URL}")
    
    # Crear todas las tablas
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas exitosamente")
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {str(e)}")
        return False
    
    db = SessionLocal()
    
    try:
        # Verificar si ya hay usuarios
        existing_users = db.query(User).count()
        if existing_users > 0:
            logger.info(f"ℹ️ Base de datos ya tiene {existing_users} usuarios. Saltando inserción de datos demo.")
            return True
        
        logger.info("📝 Creando usuarios de demostración...")
        
        # Admin
        admin_user = User(
            email="admin@ecolink.com",
            full_name="Administrador EcoLink",
            hashed_password=hash_password("admin123"),
            phone="+57 300 1234567",
            address="Carrera 50 #45-100, Medellín",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        
        # Ciudadano 1
        citizen1 = User(
            email="juan@example.com",
            full_name="Juan Pérez García",
            hashed_password=hash_password("citizen123"),
            phone="+57 301 9876543",
            address="Calle 80 #50-25, Medellín",
            role=UserRole.CITIZEN,
            is_active=True
        )
        db.add(citizen1)
        
        # Ciudadano 2
        citizen2 = User(
            email="maria@example.com",
            full_name="María López Rodríguez",
            hashed_password=hash_password("citizen123"),
            phone="+57 302 5555555",
            address="Diagonal 70 #35-10, Medellín",
            role=UserRole.CITIZEN,
            is_active=True
        )
        db.add(citizen2)
        
        # Reciclador
        recycler = User(
            email="recycler@ecolink.com",
            full_name="Empresa Recicladores ABC",
            hashed_password=hash_password("recycler123"),
            phone="+57 4 2123456",
            address="Cra 45 #60-80, Medellín",
            role=UserRole.RECYCLER,
            is_active=True
        )
        db.add(recycler)
        
        db.commit()
        logger.info("✓ Usuarios creados")
        
        # Crear rutas de recolección
        logger.info("Creando rutas...")
        
        route1 = Route(
            name="Ruta Centro",
            description="Recolección en la zona centro de Medellín",
            start_location='{"lat": 6.2518, "lng": -75.5636}',
            end_location='{"lat": 6.2550, "lng": -75.5700}',
            scheduled_start=datetime.utcnow() + timedelta(hours=2),
            scheduled_end=datetime.utcnow() + timedelta(hours=6),
            vehicle_type="Camión Compactador",
            capacity_kg=8000,
            current_weight_kg=3200,
            status=RouteStatus.IN_PROGRESS,
            is_active=True
        )
        db.add(route1)
        
        route2 = Route(
            name="Ruta Envigado",
            description="Recolección en Envigado",
            start_location='{"lat": 6.1795, "lng": -75.5892}',
            end_location='{"lat": 6.1850, "lng": -75.5950}',
            scheduled_start=datetime.utcnow() + timedelta(hours=8),
            scheduled_end=datetime.utcnow() + timedelta(hours=12),
            vehicle_type="Camión",
            capacity_kg=5000,
            current_weight_kg=1500,
            status=RouteStatus.PENDING,
            is_active=True
        )
        db.add(route2)
        
        db.commit()
        logger.info("✓ Rutas creadas")
        
        # Crear puntos de acopio
        logger.info("Creando puntos de acopio...")
        
        point1 = RecyclingPoint(
            name="Centro de Reciclaje El Hueco",
            description="Centro de acopio en el corazón de Medellín",
            latitude=6.2519,
            longitude=-75.5636,
            address="Calle 49 #49-100, El Hueco",
            accepts_cardboard=True,
            accepts_plastic=True,
            accepts_glass=True,
            accepts_metal=True,
            accepts_organic=False,
            accepts_batteries=True,
            accepts_oil=False,
            accepts_electronics=False,
            current_capacity_percent=45,
            is_active=True,
            opening_time="06:00",
            closing_time="18:00",
            contact_name="Jorge Martínez",
            contact_phone="+57 300 1111111",
            contact_email="centro.ecohueco@example.com"
        )
        db.add(point1)
        
        point2 = RecyclingPoint(
            name="Punto Verde Laureles",
            description="Punto de acopio en Laureles",
            latitude=6.2370,
            longitude=-75.5980,
            address="Cra 70 #45-50, Laureles",
            accepts_cardboard=True,
            accepts_plastic=True,
            accepts_glass=False,
            accepts_metal=True,
            accepts_organic=False,
            accepts_batteries=False,
            accepts_oil=True,
            accepts_electronics=False,
            current_capacity_percent=60,
            is_active=True,
            opening_time="07:00",
            closing_time="19:00",
            contact_name="Catalina Rojas",
            contact_phone="+57 301 2222222",
            contact_email="puntoverde.laureles@example.com"
        )
        db.add(point2)
        
        point3 = RecyclingPoint(
            name="Ecoideal Envigado",
            description="Centro especializado en electrónica",
            latitude=6.1795,
            longitude=-75.5892,
            address="Cra 48 #30-15, Envigado",
            accepts_cardboard=False,
            accepts_plastic=False,
            accepts_glass=False,
            accepts_metal=False,
            accepts_organic=False,
            accepts_batteries=True,
            accepts_oil=False,
            accepts_electronics=True,
            current_capacity_percent=25,
            is_active=True,
            opening_time="08:00",
            closing_time="17:00",
            contact_name="Ricardo Soto",
            contact_phone="+57 302 3333333",
            contact_email="ecoideal@example.com"
        )
        db.add(point3)
        
        db.commit()
        logger.info("✓ Puntos de acopio creados")
        
        # Crear logros/achievements
        logger.info("Creando logros...")
        from app.models.gamification import Achievement
        
        achievement1 = Achievement(
            name="Primer Reciclaje",
            description="Realiza tu primer reciclaje",
            icon="🌱",
            criteria="Realiza una colección",
            points_reward=50
        )
        db.add(achievement1)
        
        achievement2 = Achievement(
            name="Eco Warrior",
            description="Realiza 10 colecciones",
            icon="💪",
            criteria="Realiza 10 colecciones",
            points_reward=500
        )
        db.add(achievement2)
        
        achievement3 = Achievement(
            name="Sustentable",
            description="Recicla más de 100kg",
            icon="♻️",
            criteria="Recicla más de 100kg",
            points_reward=1000
        )
        db.add(achievement3)
        
        db.commit()
        logger.info("✓ Logros creados")
        
        # Crear stats de gamificación para usuarios
        logger.info("Inicializando estadísticas de gamificación...")
        from app.models.gamification import UserGamification
        
        for user in [citizen1, citizen2]:
            game_stats = UserGamification(
                user_id=user.id,
                total_points=250,
                points_this_month=250,
                points_this_week=100,
                level=2,
                experience=150,
                total_collections=5,
                total_weight_kg=25,
                total_recycling_points_visited=3,
                current_rank=None
            )
            db.add(game_stats)
        
        db.commit()
        logger.info("✓ Estadísticas de gamificación inicializadas")
        
        logger.info("\n✨ Base de datos inicializada exitosamente!")
        logger.info("\n📝 Usuarios de prueba:")
        logger.info("   Admin:    admin@ecolink.com / admin123")
        logger.info("   Ciudadano 1: juan@example.com / citizen123")
        logger.info("   Ciudadano 2: maria@example.com / citizen123")
        logger.info("   Reciclador: recycler@ecolink.com / recycler123")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error inicializando BD: {e}", exc_info=True)
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
