"""
ecolink/state.py
Estado global de EcoLink con tipos correctos para Reflex moderno.
Usa rx.Base en lugar de dict para listas usadas en rx.foreach.
"""

from __future__ import annotations
import reflex as rx
from sqlmodel import select, desc
from pydantic import BaseModel

from ecolink.models.db import (
    User, CollectionRoute, PickupRequest,
    CollectionPoint, RecyclingHistory, Reward, RewardClaim,
)
from ecolink.utils.auth import (
    hash_password, verify_password,
    make_session_token, verify_session_token,
    generate_claim_code,
)

PTS_PICKUP = 30

WASTE_TYPES = [
    "plástico", "orgánico", "vidrio", "papel",
    "electronico", "pilas", "aceite", "ropa", "general",
]

# ─── CLASES TIPADAS para rx.foreach ──────────────────────────────────────────
# Reflex moderno NO acepta list[dict] — requiere list[rx.Base]

class RouteItem(BaseModel):
    id: int = 0
    name: str = ""
    waste_type: str = ""
    status: str = ""
    zone: str = ""
    desc: str = ""

class PointItem(rx.Base):
    id: int = 0
    name: str = ""
    address: str = ""
    lat: float = 0.0
    lng: float = 0.0
    types: str = ""
    schedule: str = ""
    pts: int = 0
    phone: str = ""

class RewardItem(rx.Base):
    id: int = 0
    title: str = ""
    desc: str = ""
    pts: int = 0
    reward_type: str = ""
    partner: str = ""
    stock: int = 0

class HistoryItem(rx.Base):
    id: int = 0
    action_type: str = ""
    desc: str = ""
    pts: int = 0
    waste: str = ""
    date: str = ""

class PickupItem(rx.Base):
    id: int = 0
    address: str = ""
    waste: str = ""
    status: str = ""
    pts: int = 0
    date: str = ""

class RankItem(rx.Base):
    rank: int = 0
    id: int = 0
    name: str = ""
    level: str = ""
    points: int = 0
    actions: int = 0


class State(rx.State):
    """Estado global único de la aplicación EcoLink."""

    # ── Sesión (LocalStorage para persistir entre recargas) ───────────────
    _session_token: str = rx.LocalStorage("", name="ecolink_token")

    # ── Datos del usuario activo ──────────────────────────────────────────
    user_id:      int  = 0
    user_name:    str  = ""
    user_email:   str  = ""
    user_role:    str  = ""
    user_points:  int  = 0
    user_level:   str  = ""
    user_actions: int  = 0
    is_logged_in: bool = False

    # ── UI global ─────────────────────────────────────────────────────────
    is_loading:   bool = False
    notification: str  = ""
    notif_type:   str  = "info"

    # ── Formularios auth ──────────────────────────────────────────────────
    f_login_email: str = ""
    f_login_pass:  str = ""
    f_reg_name:    str = ""
    f_reg_email:   str = ""
    f_reg_pass:    str = ""

    # ── Formulario recogida ───────────────────────────────────────────────
    f_pickup_address:    str = ""
    f_pickup_waste_type: str = "plástico"
    f_pickup_notes:      str = ""

    # ── Formulario admin: ruta ────────────────────────────────────────────
    f_route_name:  str = ""
    f_route_waste: str = "plástico"
    f_route_zone:  str = ""
    f_route_desc:  str = ""

    # ── Formulario admin: punto de acopio ─────────────────────────────────
    f_point_name:     str = ""
    f_point_address:  str = ""
    f_point_lat:      str = "20.9674"
    f_point_lng:      str = "-89.5926"
    f_point_types:    str = "pilas,aceite"
    f_point_schedule: str = "Lun-Vie 9:00-18:00"
    f_point_pts:      str = "50"

    # ── Listas tipadas para rx.foreach ────────────────────────────────────
    routes:     list[RouteItem]   = []
    points:     list[PointItem]   = []
    rewards:    list[RewardItem]  = []
    history:    list[HistoryItem] = []
    my_pickups: list[PickupItem]  = []
    ranking:    list[RankItem]    = []

    # ── Stats simples (sin foreach) ───────────────────────────────────────
    stats_points:   int = 0
    stats_actions:  int = 0
    stats_pickups:  int = 0
    stats_dropoffs: int = 0
    stats_earned:   int = 0

    # ─── SETTERS ──────────────────────────────────────────────────────────

    def set_f_login_email(self, v):       self.f_login_email = v
    def set_f_login_pass(self, v):        self.f_login_pass = v
    def set_f_reg_name(self, v):          self.f_reg_name = v
    def set_f_reg_email(self, v):         self.f_reg_email = v
    def set_f_reg_pass(self, v):          self.f_reg_pass = v
    def set_f_pickup_address(self, v):    self.f_pickup_address = v
    def set_f_pickup_waste_type(self, v): self.f_pickup_waste_type = v
    def set_f_pickup_notes(self, v):      self.f_pickup_notes = v
    def set_f_route_name(self, v):        self.f_route_name = v
    def set_f_route_waste(self, v):       self.f_route_waste = v
    def set_f_route_zone(self, v):        self.f_route_zone = v
    def set_f_route_desc(self, v):        self.f_route_desc = v
    def set_f_point_name(self, v):        self.f_point_name = v
    def set_f_point_address(self, v):     self.f_point_address = v
    def set_f_point_lat(self, v):         self.f_point_lat = v
    def set_f_point_lng(self, v):         self.f_point_lng = v
    def set_f_point_types(self, v):       self.f_point_types = v
    def set_f_point_schedule(self, v):    self.f_point_schedule = v
    def set_f_point_pts(self, v):         self.f_point_pts = v
    def clear_notification(self):         self.notification = ""

    def _notify(self, msg: str, kind: str = "info"):
        self.notification = msg
        self.notif_type   = kind

# ─────────────────────────────────────────────────────────────────────────────
# SESIÓN
# ───────────────────────────────────────────────────────────────────────────

def on_load(self):
    """Restaura sesión desde LocalStorage al cargar cualquier página."""
    if self._session_token and not self.is_logged_in:
        uid = verify_session_token(self._session_token)
        if uid:
            with rx.session() as db:
                user = db.get(User, uid)
                if user and user.is_active:
                    self._load_user_state(user)
    return None

def _load_user_state(self, user: User):
    # Corregido: Quitando espacios en blanco en las asignaciones
    self.user_id = user.id
    self.user_name = user.full_name
    self.user_email = user.email
    self.user_role = user.role
    self.user_points = user.total_points
    self.user_level = user.level
    self.user_actions = user.recycling_actions
    self.is_logged_in = True

# ───────────────────────────────────────────────────────────────────────────
# AUTENTICACIÓN
# ───────────────────────────────────────────────────────────────────────────
def login(self):
    self.is_loading = True
    self.notification = ""
    with rx.session() as db:
        user = db.exec(
            select(User).where(User.email == self.f_login_email.strip().lower())
        ).first()
        
        if not user or not verify_password(self.f_login_pass, user.hashed_password):
            self.is_loading = False
            self._notify("❌ Email o contraseña incorrectos", "error")
            return
        if not user.is_active:
            self.is_loading = False
            self._notify("❌ Cuenta desactivada", "error")
            return
        
        self._load_user_state(user)
        self._session_token = make_session_token(user.id)
        self.is_loading = False
        self.f_login_pass = ""
        yield State.load_dashboard_data()
        return rx.redirect("/dashboard")

def register(self):
    self.is_loading = True
    self.notification = ""
    name = self.f_reg_name.strip()
    email = self.f_reg_email.strip().lower()
    pw = self.f_reg_pass
    
    if not name or not email or not pw:
        self._notify("⚠️ Completa todos los campos", "error")
        self.is_loading = False
        return
    if len(pw) < 6:
        self._notify("⚠️ La contraseña debe tener al menos 6 caracteres", "error")
        self.is_loading = False
        return

    with rx.session() as db:
        if db.exec(select(User).where(User.email == email)).first():
            self._notify("❌ Ese email ya está registrado", "error")
            self.is_loading = False
            return
            
        user = User(
            email=email,
            full_name=name,
            hashed_password=hash_password(pw),
            role="citizen",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        self._load_user_state(user)
        self._session_token = make_session_token(user.id)
        self.is_loading = False
        self.f_reg_pass = ""
        yield State.load_dashboard_data()
        return rx.redirect("/dashboard")

def logout(self):
    # Corregido: Quitando espacios en blanco y formateando
    self.is_logged_in = False
    self.user_id = 0
    self.user_name = ""
    self._session_token = ""
    # Resetear listas o dejarlas vacías según sea necesario
    self.routes = []
    self.points = []
    self.rewards = []
    self.history = []
    self.my_pickups = []
    self.ranking = []
    return rx.redirect("/login")

# ───────────────────────────────────────────────────────────────────────────
# CARGA DE DATOS
# ───────────────────────────────────────────────────────────────────────────
def load_dashboard_data(self):
    if not self.is_logged_in:
        return rx.redirect("/login")
    self._load_routes()
    self._load_points()
    self._load_rewards()
    self._load_history()
    self._load_pickups()
    self._load_ranking()

def _load_routes(self):
    with rx.session() as db:
        rows = db.exec(
            select(CollectionRoute).order_by(desc(CollectionRoute.created_at))
        ).all()
        self.routes = [
            RouteItem(
                id=r.id,
                name=r.name,
                waste_type=r.waste_type,
                status=r.status,
                zone=r.zone or "—",
                desc=r.description or "",
            )
            for r in rows
        ]

def _load_points(self):
    with rx.session() as db:
        rows = db.exec(
            select(CollectionPoint).where(CollectionPoint.is_active)
        ).all()
        self.points = [
            PointItem(
                id=p.id,
                name=p.name,
                address=p.address,
                lat=p.latitude,
                lng=p.longitude,
                types=p.waste_types,
                schedule=p.schedule or "Consultar",
                pts=p.points_per_visit,
                phone=p.phone or "",
            )
            for p in rows
        ]

def _load_rewards(self):
    with rx.session() as db:
        rows = db.exec(
            select(Reward).where(Reward.is_active)
            .order_by(Reward.points_required)
        ).all()
        self.rewards = [
            RewardItem(
                id=rw.id,
                title=rw.title,
                desc=rw.description or "",
                pts=rw.points_required,
                reward_type=rw.reward_type,
                partner=rw.partner_name or "",
                stock=rw.stock,
            )
            for rw in rows
        ]

def _load_history(self):
    with rx.session() as db:
        rows = db.exec(
            select(RecyclingHistory)
            .where(RecyclingHistory.user_id == self.user_id)
            .order_by(desc(RecyclingHistory.created_at))
            .limit(30)
        ).all()
        self.history = [
            HistoryItem(
                id=h.id,
                action_type=h.action_type,
                desc=h.description or "",
                pts=h.points_earned,
                waste=h.waste_type or "—",
                date=h.created_at.strftime("%d/%m/%Y %H:%M"),
            )
            for h in rows
        ]

def _load_pickups(self):
    with rx.session() as db:
        rows = db.exec(
            select(PickupRequest)
            .where(PickupRequest.user_id == self.user_id)
            .order_by(desc(PickupRequest.created_at))
            .limit(20)
        ).all()
        self.my_pickups = [
            PickupItem(
                id=p.id,
                address=p.address,
                waste=p.waste_type,
                status=p.status,
                pts=p.points_awarded,
                date=p.created_at.strftime("%d/%m/%Y"),
            )
            for p in rows
        ]

def _load_ranking(self):
    with rx.session() as db:
        rows = db.exec(
            select(User)
            .where(User.is_active)
            .order_by(desc(User.total_points))
            .limit(10)
        ).all()
        self.ranking = [
            RankItem(
                rank=i + 1,
                id=u.id,
                name=u.full_name,
                level=u.level,
                points=u.total_points,
                actions=u.recycling_actions,
            )
            for i, u in enumerate(rows)
        ]

# ───────────────────────────────────────────────────────────────────────────
# ACCIONES CIUDADANO
# ───────────────────────────────────────────────────────────────────────────
def request_pickup(self):
    if not self.f_pickup_address.strip():
        self._notify("⚠️ Escribe tu dirección", "error")
        return

    with rx.session() as db:
        pickup = PickupRequest(
            user_id=self.user_id,
            address=self.f_pickup_address.strip(),
            waste_type=self.f_pickup_waste_type,
            notes=self.f_pickup_notes.strip() or None,
            points_awarded=PTS_PICKUP,
        )
        db.add(pickup)
        
        user = db.get(User, self.user_id)
        level_up = user.add_points(PTS_PICKUP)
        db.add(user)
        
        hist = RecyclingHistory(
            user_id=self.user_id,
            action_type="pickup",
            description=f"Recogida solicitada en: {self.f_pickup_address.strip()}",
            points_earned=PTS_PICKUP,
            waste_type=self.f_pickup_waste_type,
        )
        db.add(hist)
        
        db.commit()
        db.refresh(user)
        
        self.user_points = user.total_points
        self.user_level = user.level
        self.user_actions = user.recycling_actions
        
        msg = f"✅ Recogida registrada. +{PTS_PICKUP} puntos"
        if level_up:
            msg += f" 🎉 ¡Subiste a nivel {self.user_level}!"
        
        self._notify(msg, "success")
        self.f_pickup_address = ""
        self.f_pickup_notes = ""
        self._load_pickups()
        self._load_history()

def register_dropoff(self, point_id: int):
    with rx.session() as db:
        point = db.get(CollectionPoint, point_id)
        if not point:
            self._notify("❌ Punto no encontrado", "error")
            return
        
        pts = point.points_per_visit
        user = db.get(User, self.user_id)
        level_up = user.add_points(pts)
        db.add(user)
        
        hist = RecyclingHistory(
            user_id=self.user_id,
            action_type="dropoff",
            description=f"Residuos entregados en: {point.name}",
            points_earned=pts,
            waste_type="general",
        )
        db.add(hist)
        
        db.commit()
        db.refresh(user)
        
        self.user_points = user.total_points
        self.user_level = user.level
        self.user_actions = user.recycling_actions
        
        point_name = point.name
        msg = f"🎉 +{pts} puntos por visitar {point_name}"
        if level_up:
            msg += f" · ¡Nuevo nivel: {self.user_level}!"
            
        self._notify(msg, "success")
        self._load_history()

def claim_reward(self, reward_id: int):
    with rx.session() as db:
        reward = db.get(Reward, reward_id)
        if not reward or not reward.is_active:
            self._notify("❌ Recompensa no disponible", "error")
            return
        if reward.stock == 0:
            self._notify("❌ Sin stock disponible", "error")
            return
        
        user = db.get(User, self.user_id)
        if user.total_points < reward.points_required:
            self._notify(
                f"❌ Necesitas {reward.points_required} pts. Tienes {user.total_points}",
                "error",
            )
            return
            
        user.total_points -= reward.points_required
        user._recalc_level()
        db.add(user)
        
        if reward.stock > 0:
            reward.stock -= 1
            db.add(reward)
            
        claim = RewardClaim(
            user_id=self.user_id,
            reward_id=reward_id,
            points_spent=reward.points_required,
            code=generate_claim_code(),
        )
        db.add(claim)
        
        db.commit()
        db.refresh(user)
        db.refresh(claim)
        
        self.user_points = user.total_points
        self.user_level = user.level
        code = claim.code
        self._notify(f"🎁 Canjeado. Tu código: {code}", "success")
        self._load_rewards()

# ───────────────────────────────────────────────────────────────────────────
# ACCIONES ADMIN
# ───────────────────────────────────────────────────────────────────────────
def create_route(self):
    if self.user_role != "admin":
        self._notify("❌ Solo administradores", "error")
        return
    if not self.f_route_name.strip():
        self._notify("⚠️ Escribe el nombre de la ruta", "error")
        return
        
    with rx.session() as db:
        db.add(CollectionRoute(
            name=self.f_route_name.strip(),
            waste_type=self.f_route_waste,
            zone=self.f_route_zone.strip() or None,
            description=self.f_route_desc.strip() or None,
        ))
        db.commit()
        self._notify(f"✅ Ruta '{self.f_route_name}' creada", "success")
        self.f_route_name = ""
        self.f_route_zone = ""
        self.f_route_desc = ""
        self._load_routes()

def update_route_status(self, route_id: int, new_status: str):
    if self.user_role != "admin":
        return
    with rx.session() as db:
        route = db.get(CollectionRoute, route_id)
        if route:
            route.status = new_status
            db.add(route)
            db.commit()
            self._notify(f"✅ Estado → '{new_status}'", "success")
            self._load_routes()

def create_point(self):
    if self.user_role != "admin":
        self._notify("❌ Solo administradores", "error")
        return
    if not self.f_point_name.strip():
        self._notify("⚠️ Escribe el nombre del punto", "error")
        return
        
    try:
        lat = float(self.f_point_lat)
        lng = float(self.f_point_lng)
        pts = int(self.f_point_pts)
    except ValueError:
        self._notify("⚠️ Latitud, longitud y puntos deben ser números", "error")
        return
        
    with rx.session() as db:
        db.add(CollectionPoint(
            name=self.f_point_name.strip(),
            address=self.f_point_address.strip(),
            latitude=lat,
            longitude=lng,
            waste_types=self.f_point_types.strip(),
            schedule=self.f_point_schedule.strip() or None,
            points_per_visit=pts,
        ))
        db.commit()
        self._notify(f"✅ Punto '{self.f_point_name}' creado", "success")
        self.f_point_name = ""
        self.f_point_address = ""
        self._load_points()

# ───────────────────────────────────────────────────────────────────────────
# SEED DE DATOS DEMO
# ───────────────────────────────────────────────────────────────────────────
def seed_if_empty(self):
    """Inserta datos demo si la BD está vacía."""
    with rx.session() as db:
        if db.exec(select(CollectionRoute)).first():
            return
        
        # Rutas
        for name, waste, zone, status in [
            ("Ruta Norte · Plástico", "plástico", "Centro Norte", "in_progress"),
            ("Ruta Sur · Orgánico", "orgánico", "Col. Sur", "scheduled"),
            ("Ruta Este · Vidrio", "vidrio", "Zona Industrial", "scheduled"),
            ("Ruta Oeste · Papel", "papel", "Frac. Bello", "scheduled"),
        ]:
            db.add(CollectionRoute(name=name, waste_type=waste, zone=zone, status=status))
            
        # Puntos de recolección
        for nm, addr, lat, lng, types, sch, pts in [
            ("Centro Acopio Municipal", "Calle 60 #500, Centro", 20.9674, -89.5926, "pilas,aceite,plastico,vidrio,papel", "Lun-Sáb 8:00-17:00", 60),
            ("Punto Verde Altabrisa", "Av. Altabrisa #200", 21.0012, -89.6145, "pilas,electronico,ropa", "Lun-Vie 9:00-18:00", 50),
            ("Ecocentro Gran Plaza", "Gran Plaza, Mérida", 20.9856, -89.6234, "plastico,papel,vidrio", "Todos los días 10:00-21:00", 40),
            ("Recolección Aceite", "Calle 21 #301, Col. Méx", 20.9523, -89.5789, "aceite", "Mié y Vie 9:00-14:00", 70),
        ]:
            db.add(CollectionPoint(
                name=nm,
                address=addr,
                latitude=lat,
                longitude=lng,
                waste_types=types,
                schedule=sch,
                points_per_visit=pts,
            ))
            
        # Recompensas
        for title, desc, pts, rtype, disc, partner in [
            ("10% desc. en El Giro", "Descuento en toda la carta.", 100, "discount", 10.0, "Restaurante El Giro"),
            ("Bolsa ecológica reutilizable", "Bolsa de tela con logo EcoLink.", 200, "benefit", None, "Municipio de Mérida"),
            ("Mes gratis transporte", "Saldo para 30 días de autobús.", 500, "municipal", None, "TAME Mérida"),
            ("Certificado Ciudadano Eco", "Reconocimiento oficial.", 800, "certificate", None, "Municipio de Mérida"),
            ("20% en Oxxo Gas", "Descuento en tu próxima carga.", 300, "discount", 20.0, "Oxxo Gas"),
        ]:
            db.add(Reward(
                title=title,
                description=desc,
                points_required=pts,
                reward_type=rtype,
                discount_percent=disc,
                partner_name=partner,
            ))
        
        # Cometer los cambios
        db.commit()