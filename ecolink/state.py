"""
ecolink/state.py
Estado global de EcoLink con tipos correctos para Reflex moderno.
"""

from __future__ import annotations
import json as _json
import reflex as rx
from sqlmodel import select, desc

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

ZONE_WAYPOINTS: dict[str, list[dict]] = {
    "Centro Norte": [
        {"lat": 20.9674, "lng": -89.5926}, {"lat": 20.9695, "lng": -89.5940},
        {"lat": 20.9712, "lng": -89.5955}, {"lat": 20.9730, "lng": -89.5965},
        {"lat": 20.9748, "lng": -89.5950}, {"lat": 20.9760, "lng": -89.5932},
        {"lat": 20.9745, "lng": -89.5910}, {"lat": 20.9720, "lng": -89.5900},
    ],
    "Col. Sur": [
        {"lat": 20.9520, "lng": -89.5890}, {"lat": 20.9505, "lng": -89.5910},
        {"lat": 20.9488, "lng": -89.5930}, {"lat": 20.9470, "lng": -89.5945},
        {"lat": 20.9455, "lng": -89.5960}, {"lat": 20.9440, "lng": -89.5975},
        {"lat": 20.9460, "lng": -89.5995}, {"lat": 20.9480, "lng": -89.5980},
    ],
    "Zona Industrial": [
        {"lat": 20.9800, "lng": -89.5600}, {"lat": 20.9820, "lng": -89.5580},
        {"lat": 20.9840, "lng": -89.5560}, {"lat": 20.9860, "lng": -89.5545},
        {"lat": 20.9880, "lng": -89.5530}, {"lat": 20.9870, "lng": -89.5510},
        {"lat": 20.9850, "lng": -89.5525},
    ],
    "Frac. Bello": [
        {"lat": 20.9900, "lng": -89.6100}, {"lat": 20.9920, "lng": -89.6120},
        {"lat": 20.9940, "lng": -89.6140}, {"lat": 20.9955, "lng": -89.6160},
        {"lat": 20.9940, "lng": -89.6180}, {"lat": 20.9920, "lng": -89.6170},
        {"lat": 20.9905, "lng": -89.6150},
    ],
    "Altabrisa": [
        {"lat": 21.0010, "lng": -89.6140}, {"lat": 21.0030, "lng": -89.6155},
        {"lat": 21.0050, "lng": -89.6170}, {"lat": 21.0065, "lng": -89.6185},
        {"lat": 21.0055, "lng": -89.6200}, {"lat": 21.0035, "lng": -89.6190},
        {"lat": 21.0015, "lng": -89.6175},
    ],
    "García Ginerés": [
        {"lat": 20.9760, "lng": -89.6100}, {"lat": 20.9775, "lng": -89.6115},
        {"lat": 20.9790, "lng": -89.6130}, {"lat": 20.9805, "lng": -89.6120},
        {"lat": 20.9815, "lng": -89.6105}, {"lat": 20.9800, "lng": -89.6090},
        {"lat": 20.9780, "lng": -89.6085},
    ],
    "Itzimná": [
        {"lat": 20.9850, "lng": -89.6200}, {"lat": 20.9865, "lng": -89.6215},
        {"lat": 20.9880, "lng": -89.6230}, {"lat": 20.9895, "lng": -89.6220},
        {"lat": 20.9885, "lng": -89.6200}, {"lat": 20.9870, "lng": -89.6185},
    ],
    "Uman": [
        {"lat": 20.8900, "lng": -89.7520}, {"lat": 20.8920, "lng": -89.7540},
        {"lat": 20.8940, "lng": -89.7555}, {"lat": 20.8960, "lng": -89.7570},
        {"lat": 20.8945, "lng": -89.7590}, {"lat": 20.8925, "lng": -89.7580},
    ],
}

ROUTE_ZONES = list(ZONE_WAYPOINTS.keys())


# ─── Modelos serializables para el frontend ───────────────────────────────────

class RouteItem(rx.Base):
    id: int = 0
    name: str = ""
    waste_type: str = ""
    status: str = ""
    zone: str = ""
    desc: str = ""
    current_lat: float = 0.0
    current_lng: float = 0.0

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


# ─── Estado Principal ─────────────────────────────────────────────────────────

class State(rx.State):

    _session_token: str = rx.LocalStorage("", name="ecolink_token")

    user_id:      int  = 0
    user_name:    str  = ""
    user_email:   str  = ""
    user_role:    str  = ""
    user_points:  int  = 0
    user_level:   str  = ""
    user_actions: int  = 0
    is_logged_in: bool = False

    is_loading:   bool = False
    notification: str  = ""
    notif_type:   str  = "info"

    f_login_email: str = ""
    f_login_pass:  str = ""
    f_reg_name:    str = ""
    f_reg_email:   str = ""
    f_reg_pass:    str = ""

    f_pickup_address:    str = ""
    f_pickup_waste_type: str = "plástico"
    f_pickup_notes:      str = ""

    f_route_name:  str = ""
    f_route_waste: str = "plástico"
    f_route_zone:  str = ""
    f_route_desc:  str = ""

    f_point_name:     str = ""
    f_point_address:  str = ""
    f_point_lat:      str = "20.9674"
    f_point_lng:      str = "-89.5926"
    f_point_types:    str = "pilas,aceite"
    f_point_schedule: str = "Lun-Vie 9:00-18:00"
    f_point_pts:      str = "50"

    routes:     list[RouteItem]   = []
    points:     list[PointItem]   = []
    rewards:    list[RewardItem]  = []
    history:    list[HistoryItem] = []
    my_pickups: list[PickupItem]  = []
    ranking:    list[RankItem]    = []

    stats_points:   int = 0
    stats_actions:  int = 0
    stats_pickups:  int = 0
    stats_dropoffs: int = 0
    stats_earned:   int = 0

    # ─── Apoyo ────────────────────────────────────────────────────────────────

    def _notify(self, msg: str, kind: str = "info"):
        self.notification = msg
        self.notif_type   = kind

    def clear_notification(self):
        self.notification = ""

    # ─── Sesión ───────────────────────────────────────────────────────────────

    def on_load(self):
        if self._session_token and not self.is_logged_in:
            uid = verify_session_token(self._session_token)
            if uid:
                with rx.session() as db:
                    user = db.get(User, uid)
                    if user and user.is_active:
                        self._load_user_state(user)

    def _load_user_state(self, user: User):
        self.user_id      = user.id
        self.user_name    = user.full_name
        self.user_email   = user.email
        self.user_role    = user.role
        self.user_points  = user.total_points
        self.user_level   = user.level
        self.user_actions = user.recycling_actions
        self.is_logged_in = True

    # ─── Auth ─────────────────────────────────────────────────────────────────

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
            return rx.redirect("/dashboard")

    def register_user(self):
        self.is_loading = True
        self.notification = ""
        name  = self.f_reg_name.strip()
        email = self.f_reg_email.strip().lower()
        pw    = self.f_reg_pass
        if not name or not email or not pw:
            self._notify("⚠️ Completa todos los campos", "error")
            self.is_loading = False
            return
        if len(pw) < 6:
            self._notify("⚠️ Contraseña mínimo 6 caracteres", "error")
            self.is_loading = False
            return
        with rx.session() as db:
            if db.exec(select(User).where(User.email == email)).first():
                self._notify("❌ Ese email ya está registrado", "error")
                self.is_loading = False
                return
            user = User(email=email, full_name=name, hashed_password=hash_password(pw), role="citizen")
            db.add(user)
            db.commit()
            db.refresh(user)
            self._load_user_state(user)
            self._session_token = make_session_token(user.id)
            self.is_loading = False
            self.f_reg_pass = self.f_reg_name = self.f_reg_email = ""
            self._notify("✅ Cuenta creada. Inicia sesión.", "success")
            return rx.redirect("/login")

    def logout(self):
        self.is_logged_in = False
        self.user_id      = 0
        self.user_name    = ""
        self._session_token = ""
        self.routes = self.points = self.rewards = []
        self.history = self.my_pickups = self.ranking = []
        return rx.redirect("/login")

    # ─── Carga de datos ───────────────────────────────────────────────────────

    @rx.event
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
            rows = db.exec(select(CollectionRoute).order_by(desc(CollectionRoute.created_at))).all()
            self.routes = [
                RouteItem(
                    id=r.id, name=r.name, waste_type=r.waste_type,
                    status=r.status, zone=r.zone or "—", desc=r.description or "",
                    current_lat=r.current_lat or 0.0,
                    current_lng=r.current_lng or 0.0,
                )
                for r in rows
            ]

    def _load_points(self):
        with rx.session() as db:
            rows = db.exec(select(CollectionPoint).where(CollectionPoint.is_active)).all()
            self.points = [
                PointItem(
                    id=p.id, name=p.name, address=p.address,
                    lat=p.latitude, lng=p.longitude, types=p.waste_types,
                    schedule=p.schedule or "Consultar",
                    pts=p.points_per_visit, phone=p.phone or "",
                )
                for p in rows
            ]

    def _load_rewards(self):
        with rx.session() as db:
            rows = db.exec(select(Reward).where(Reward.is_active).order_by(Reward.points_required)).all()
            self.rewards = [
                RewardItem(
                    id=rw.id, title=rw.title, desc=rw.description or "",
                    pts=rw.points_required, reward_type=rw.reward_type,
                    partner=rw.partner_name or "", stock=rw.stock,
                )
                for rw in rows
            ]

    def _load_history(self):
        with rx.session() as db:
            rows = db.exec(
                select(RecyclingHistory)
                .where(RecyclingHistory.user_id == self.user_id)
                .order_by(desc(RecyclingHistory.created_at)).limit(30)
            ).all()
            self.history = [
                HistoryItem(
                    id=h.id, action_type=h.action_type, desc=h.description or "",
                    pts=h.points_earned, waste=h.waste_type or "—",
                    date=h.created_at.strftime("%d/%m/%Y %H:%M"),
                )
                for h in rows
            ]

    def _load_pickups(self):
        with rx.session() as db:
            rows = db.exec(
                select(PickupRequest)
                .where(PickupRequest.user_id == self.user_id)
                .order_by(desc(PickupRequest.created_at)).limit(20)
            ).all()
            self.my_pickups = [
                PickupItem(
                    id=p.id, address=p.address, waste=p.waste_type,
                    status=p.status, pts=p.points_awarded,
                    date=p.created_at.strftime("%d/%m/%Y"),
                )
                for p in rows
            ]

    def _load_ranking(self):
        with rx.session() as db:
            rows = db.exec(
                select(User).where(User.is_active)
                .order_by(desc(User.total_points)).limit(10)
            ).all()
            self.ranking = [
                RankItem(rank=i+1, id=u.id, name=u.full_name,
                         level=u.level, points=u.total_points, actions=u.recycling_actions)
                for i, u in enumerate(rows)
            ]

    # ─── Acciones ciudadano ───────────────────────────────────────────────────

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
                user_id=self.user_id, action_type="pickup",
                description=f"Recogida solicitada en: {self.f_pickup_address.strip()}",
                points_earned=PTS_PICKUP, waste_type=self.f_pickup_waste_type,
            )
            db.add(hist)
            db.commit()
            db.refresh(user)
            self.user_points  = user.total_points
            self.user_level   = user.level
            self.user_actions = user.recycling_actions
            msg = f"✅ Recogida registrada. +{PTS_PICKUP} puntos"
            if level_up:
                msg += f" 🎉 ¡Subiste a nivel {self.user_level}!"
            self._notify(msg, "success")
            self.f_pickup_address = ""
            self.f_pickup_notes   = ""
            self._load_pickups()
            self._load_history()

    def register_dropoff(self, point_id: int):
        with rx.session() as db:
            point = db.get(CollectionPoint, point_id)
            if not point:
                self._notify("❌ Punto no encontrado", "error")
                return
            pts  = point.points_per_visit
            user = db.get(User, self.user_id)
            level_up = user.add_points(pts)
            db.add(user)
            hist = RecyclingHistory(
                user_id=self.user_id, action_type="dropoff",
                description=f"Residuos entregados en: {point.name}",
                points_earned=pts, waste_type="general",
            )
            db.add(hist)
            db.commit()
            db.refresh(user)
            self.user_points  = user.total_points
            self.user_level   = user.level
            self.user_actions = user.recycling_actions
            msg = f"🎉 +{pts} puntos por visitar {point.name}"
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
                self._notify(f"❌ Necesitas {reward.points_required} pts. Tienes {user.total_points}", "error")
                return
            user.total_points -= reward.points_required
            user._recalc_level()
            db.add(user)
            if reward.stock > 0:
                reward.stock -= 1
                db.add(reward)
            claim = RewardClaim(
                user_id=self.user_id, reward_id=reward_id,
                points_spent=reward.points_required, code=generate_claim_code(),
            )
            db.add(claim)
            db.commit()
            db.refresh(user)
            self.user_points = user.total_points
            self.user_level  = user.level
            self._notify(f"🎁 Canjeado. Tu código: {claim.code}", "success")
            self._load_rewards()

    # ─── Acciones admin ───────────────────────────────────────────────────────

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
            self.f_route_name = self.f_route_zone = self.f_route_desc = ""
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
                latitude=lat, longitude=lng,
                waste_types=self.f_point_types.strip(),
                schedule=self.f_point_schedule.strip() or None,
                points_per_visit=pts,
            ))
            db.commit()
            self._notify(f"✅ Punto '{self.f_point_name}' creado", "success")
            self.f_point_name = self.f_point_address = ""
            self._load_points()

    # ─── Simulación de rutas ──────────────────────────────────────────────────

    def start_route_simulation(self, route_id: int):
        """Admin inicia la simulación: pone el camión en el primer waypoint."""
        if self.user_role != "admin":
            self._notify("❌ Solo administradores", "error")
            return
        with rx.session() as db:
            route = db.get(CollectionRoute, route_id)
            if not route:
                self._notify("❌ Ruta no encontrada", "error")
                return
            zone = route.zone or "Centro Norte"
            waypoints = ZONE_WAYPOINTS.get(zone, list(ZONE_WAYPOINTS.values())[0])
            route.waypoints_json = _json.dumps(waypoints)
            route.status = "in_progress"
            route.current_lat = waypoints[0]["lat"]
            route.current_lng = waypoints[0]["lng"]
            db.add(route)
            db.commit()
            name = route.name
        self._notify(f"🚛 Ruta iniciada · {name}", "success")
        self._load_routes()

    def advance_truck(self, route_id: int):
        """Avanza el camión al siguiente waypoint."""
        with rx.session() as db:
            route = db.get(CollectionRoute, route_id)
            if not route or route.status != "in_progress":
                return
            waypoints = _json.loads(route.waypoints_json or "[]")
            if not waypoints:
                return
            cur_lat = route.current_lat or waypoints[0]["lat"]
            cur_lng = route.current_lng or waypoints[0]["lng"]
            current_idx = 0
            for i, wp in enumerate(waypoints):
                if abs(wp["lat"] - cur_lat) < 0.0001 and abs(wp["lng"] - cur_lng) < 0.0001:
                    current_idx = i
                    break
            next_idx = current_idx + 1
            if next_idx >= len(waypoints):
                route.status = "completed"
                route.current_lat = waypoints[-1]["lat"]
                route.current_lng = waypoints[-1]["lng"]
                db.add(route)
                db.commit()
                self._notify("✅ Ruta completada", "success")
                self._load_routes()
                return
            route.current_lat = waypoints[next_idx]["lat"]
            route.current_lng = waypoints[next_idx]["lng"]
            db.add(route)
            db.commit()
        self._load_routes()

    def stop_route(self, route_id: int):
        """Admin detiene una ruta."""
        if self.user_role != "admin":
            return
        with rx.session() as db:
            route = db.get(CollectionRoute, route_id)
            if route:
                route.status = "cancelled"
                db.add(route)
                db.commit()
        self._notify("⛔ Ruta detenida", "info")
        self._load_routes()

    def reset_route(self, route_id: int):
        """Admin reinicia una ruta al estado programado."""
        if self.user_role != "admin":
            return
        with rx.session() as db:
            route = db.get(CollectionRoute, route_id)
            if route:
                route.status = "scheduled"
                route.current_lat = None
                route.current_lng = None
                db.add(route)
                db.commit()
        self._notify("🔄 Ruta reiniciada", "info")
        self._load_routes()

    # ─── Seed ─────────────────────────────────────────────────────────────────

    def seed_if_empty(self):
        with rx.session() as db:
            if db.exec(select(CollectionRoute)).first():
                return
            rutas_init = [
                ("Ruta Norte · Plástico", "plástico", "Centro Norte", "in_progress"),
                ("Ruta Sur · Orgánico",   "orgánico", "Col. Sur",     "scheduled"),
                ("Ruta Este · Vidrio",    "vidrio",   "Zona Industrial", "scheduled"),
                ("Ruta Oeste · Papel",    "papel",    "Frac. Bello",  "scheduled"),
            ]
            for name, waste, zone, status in rutas_init:
                db.add(CollectionRoute(name=name, waste_type=waste, zone=zone, status=status))
            puntos_init = [
                ("Centro Acopio Municipal", "Calle 60 #500, Centro", 20.9674, -89.5926, "pilas,aceite,plastico,vidrio,papel", "Lun-Sáb 8:00-17:00", 60),
                ("Punto Verde Altabrisa",  "Av. Altabrisa #200",    21.0012, -89.6145, "pilas,electronico,ropa",             "Lun-Vie 9:00-18:00", 50),
                ("Ecocentro Gran Plaza",   "Gran Plaza, Mérida",    20.9856, -89.6234, "plastico,papel,vidrio",              "Todos los días 10:00-21:00", 40),
                ("Recolección Aceite",     "Calle 21 #301, Col. Méx", 20.9523, -89.5789, "aceite",                         "Mié y Vie 9:00-14:00", 70),
            ]
            for nm, addr, lat, lng, types, sch, pts in puntos_init:
                db.add(CollectionPoint(name=nm, address=addr, latitude=lat, longitude=lng,
                                       waste_types=types, schedule=sch, points_per_visit=pts))
            rewards_init = [
                ("10% desc. en El Giro",        "Descuento en toda la carta.",                   100, "discount",    10.0, "Restaurante El Giro"),
                ("Bolsa ecológica reutilizable", "Bolsa de tela con logo EcoLink.",               200, "benefit",     None, "Municipio de Mérida"),
                ("200 pesos saldo transporte",   "Saldo para 30 días de transporte Va y Ven.",    500, "municipal",   None, "TAME Mérida"),
                ("Certificado Ciudadano Eco",    "Reconocimiento oficial.",                       800, "certificate", None, "Municipio de Mérida"),
                ("20% en Oxxo Gas",             "Descuento en tu próxima carga.",                300, "discount",    20.0, "Oxxo Gas"),
            ]
            for title, desc, pts, rtype, disc, partner in rewards_init:
                db.add(Reward(title=title, description=desc, points_required=pts,
                              reward_type=rtype, discount_percent=disc, partner_name=partner))
            db.commit()