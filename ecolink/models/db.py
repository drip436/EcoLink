"""
ecolink/models/db.py
═══════════════════════════════════════════════════════════════════════════════
Modelos de base de datos con SQLModel.
SQLModel = SQLAlchemy + Pydantic, integrado nativamente con Reflex.

Reflex expone rx.Model (que hereda de SQLModel) para definir tablas.
Todas las tablas se crean automáticamente con `reflex db migrate`.
═══════════════════════════════════════════════════════════════════════════════
"""

import datetime
import json
from typing import Optional
import reflex as rx
from sqlmodel import Field,  Column, TEXT


# ─── USUARIO ──────────────────────────────────────────────────────────────────
class User(rx.Model, table=True):
    """
    Representa a un ciudadano o administrador del sistema.
    Los puntos y nivel viven aquí para que el ranking sea un
    simple ORDER BY sin JOINs costosos.
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    hashed_password: str = Field(max_length=255)

    # citizen | admin | recycler
    role: str = Field(default="citizen", max_length=20)
    is_active: bool = Field(default=True)

    # ── Gamificación ──────────────────────────────────────────────────────
    total_points: int = Field(default=0)
    # Semilla | Brote | Hoja | Árbol | Bosque
    level: str = Field(default="Semilla", max_length=30)
    recycling_actions: int = Field(default=0)

    # Ubicación (para notificaciones de rutas cercanas)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    def add_points(self, pts: int) -> bool:
        """Suma puntos, actualiza nivel. Devuelve True si subió de nivel."""
        prev = self.level
        self.total_points += pts
        self.recycling_actions += 1
        self._recalc_level()
        return self.level != prev

    def _recalc_level(self):
        p = self.total_points
        if p >= 1500:
            self.level = "Bosque"
        elif p >= 700:
            self.level = "Árbol"
        elif p >= 300:
            self.level = "Hoja"
        elif p >= 100:
            self.level = "Brote"
        else:
            self.level = "Semilla"


# ─── RUTA DE RECOLECCIÓN ──────────────────────────────────────────────────────
class CollectionRoute(rx.Model, table=True):
    """
    Ruta que sigue el camión recolector.
    waypoints_json almacena la lista de paradas como JSON string
    (SQLModel no soporta JSON nativo en todos los dialectos).
    """
    __tablename__ = "collection_routes"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    # plástico | orgánico | vidrio | papel | electronico | pilas | aceite
    waste_type: str = Field(max_length=50)
    zone: Optional[str] = Field(default=None, max_length=100)

    # scheduled | in_progress | completed | cancelled
    status: str = Field(default="scheduled", max_length=30)

    # Posición GPS actual del camión (actualizada por admin)
    current_lat: Optional[float] = Field(default=None)
    current_lng: Optional[float] = Field(default=None)

    # JSON string: '[{"lat":20.96,"lng":-89.59,"address":"Calle 60..."}]'
    waypoints_json: Optional[str] = Field(default="[]", sa_column=Column(TEXT))

    scheduled_start: Optional[datetime.datetime] = Field(default=None)
    scheduled_end: Optional[datetime.datetime] = Field(default=None)

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    @property
    def waypoints(self) -> list:
        try:
            return json.loads(self.waypoints_json or "[]")
        except Exception:
            return []


# ─── SOLICITUD DE RECOGIDA ────────────────────────────────────────────────────
class PickupRequest(rx.Model, table=True):
    """
    El ciudadano marca que tiene residuos pendientes de recoger.
    Gana puntos al crearse la solicitud.
    """
    __tablename__ = "pickup_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    route_id: Optional[int] = Field(default=None, foreign_key="collection_routes.id")

    address: str = Field(max_length=500)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    waste_type: str = Field(max_length=50)
    notes: Optional[str] = Field(default=None, sa_column=Column(TEXT))

    # pending | confirmed | collected | cancelled
    status: str = Field(default="pending", max_length=30)
    points_awarded: int = Field(default=30)

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    collected_at: Optional[datetime.datetime] = Field(default=None)


# ─── PUNTO DE ACOPIO ──────────────────────────────────────────────────────────
class CollectionPoint(rx.Model, table=True):
    """
    Ubicación física donde los ciudadanos pueden llevar residuos especiales.
    waste_types es CSV: 'pilas,aceite,plastico'
    """
    __tablename__ = "collection_points"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    address: str = Field(max_length=500)
    latitude: float
    longitude: float
    waste_types: str = Field(max_length=500)   # CSV
    description: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    schedule: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    points_per_visit: int = Field(default=50)
    phone: Optional[str] = Field(default=None, max_length=50)

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


# ─── HISTORIAL DE RECICLAJE ───────────────────────────────────────────────────
class RecyclingHistory(rx.Model, table=True):
    """
    Log de cada acción eco-responsable del usuario.
    action_type: pickup | dropoff
    """
    __tablename__ = "recycling_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    action_type: str = Field(max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)
    points_earned: int = Field(default=0)
    waste_type: Optional[str] = Field(default=None, max_length=50)

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


# ─── RECOMPENSA ───────────────────────────────────────────────────────────────
class Reward(rx.Model, table=True):
    """
    Recompensa canjeable con puntos acumulados.
    reward_type: discount | benefit | certificate | municipal
    """
    __tablename__ = "rewards"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    points_required: int
    reward_type: str = Field(default="discount", max_length=50)
    discount_percent: Optional[float] = Field(default=None)
    partner_name: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    stock: int = Field(default=100)   # -1 = ilimitado

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


# ─── CANJE DE RECOMPENSA ──────────────────────────────────────────────────────
class RewardClaim(rx.Model, table=True):
    """Registro de cada canje realizado por un usuario."""
    __tablename__ = "reward_claims"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    reward_id: int = Field(foreign_key="rewards.id")
    points_spent: int
    code: Optional[str] = Field(default=None, max_length=50)

    # pending | approved | redeemed
    status: str = Field(default="approved", max_length=30)

    claimed_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
