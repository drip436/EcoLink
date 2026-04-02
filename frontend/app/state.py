"""
Estado Global de Reflex para EcoLink
Maneja autenticación, usuario actual, datos de rutas, puntos, etc.
"""
import reflex as rx
import httpx
from typing import Optional, List
from pydantic import BaseModel
import json

# Configuración del API
API_URL = "http://localhost:8000"


class User(BaseModel):
    """Modelo de usuario"""
    id: int
    email: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    role: str
    is_active: bool


class GamificationStats(BaseModel):
    """Estadísticas de gamificación"""
    total_points: int = 0
    level: int = 1
    total_collections: int = 0
    total_weight_kg: int = 0
    current_rank: Optional[int] = None


class RecyclingPoint(BaseModel):
    """Punto de acopio"""
    id: int
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    address: str
    current_capacity_percent: int
    is_active: bool
    waste_types: List[str] = []


class Route(BaseModel):
    """Ruta de recolección"""
    id: int
    name: str
    status: str
    scheduled_start: str
    scheduled_end: str
    current_weight_kg: int
    capacity_kg: int


class Collection(BaseModel):
    """Colección realizada"""
    id: int
    waste_type: str
    weight_kg: int
    status: str
    address: Optional[str] = None


class AppState(rx.State):
    """Estado global de EcoLink"""
    
    # Autenticación
    token: Optional[str] = None
    is_authenticated: bool = False
    current_user: Optional[User] = None
    login_email: str = ""
    login_password: str = ""
    register_email: str = ""
    register_password: str = ""
    register_full_name: str = ""
    register_confirm_password: str = ""
    auth_error: str = ""
    
    # Gamificación
    gamification_stats: Optional[GamificationStats] = None
    leaderboard: List[dict] = []
    
    # Datos de la app
    recycling_points: List[RecyclingPoint] = []
    active_routes: List[Route] = []
    my_collections: List[Collection] = []
    
    # Estado de UI
    loading: bool = False
    selected_point: Optional[RecyclingPoint] = None
    
    # Parámetros de búsqueda
    waste_type_filter: str = ""
    
    def reset_form(self):
        """Resetear formularios"""
        self.login_email = ""
        self.login_password = ""
        self.register_email = ""
        self.register_password = ""
        self.register_full_name = ""
        self.register_confirm_password = ""
        self.auth_error = ""
    
    def handle_login(self):
        """Manejar login"""
        self.loading = True
        self.auth_error = ""
        
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{API_URL}/auth/login",
                    json={
                        "email": self.login_email,
                        "password": self.login_password,
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data["access_token"]
                    self.is_authenticated = True
                    
                    # Parsear usuario
                    user_data = data["user"]
                    self.current_user = User(**user_data)
                    
                    # Obtener stats
                    self.load_gamification_stats()
                    self.load_recycling_points()
                    self.load_active_routes()
                    
                    self.reset_form()
                else:
                    self.auth_error = "Email o contraseña incorrectos"
        except Exception as e:
            self.auth_error = f"Error de conexión: {str(e)}"
        finally:
            self.loading = False
    
    def handle_register(self):
        """Manejar registro"""
        self.loading = True
        self.auth_error = ""
        
        if self.register_password != self.register_confirm_password:
            self.auth_error = "Las contraseñas no coinciden"
            self.loading = False
            return
        
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{API_URL}/auth/register",
                    json={
                        "email": self.register_email,
                        "full_name": self.register_full_name,
                        "password": self.register_password,
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data["access_token"]
                    self.is_authenticated = True
                    
                    user_data = data["user"]
                    self.current_user = User(**user_data)
                    
                    self.reset_form()
                else:
                    error_detail = response.json().get("detail", "Error en registro")
                    self.auth_error = error_detail
        except Exception as e:
            self.auth_error = f"Error: {str(e)}"
        finally:
            self.loading = False
    
    def handle_logout(self):
        """Manejar logout"""
        self.token = None
        self.is_authenticated = False
        self.current_user = None
        self.gamification_stats = None
        self.recycling_points = []
        self.active_routes = []
        self.my_collections = []
        self.reset_form()
    
    def load_recycling_points(self):
        """Cargar puntos de acopio"""
        self.loading = True
        try:
            with httpx.Client() as client:
                params = {}
                if self.waste_type_filter:
                    params["waste_type"] = self.waste_type_filter.lower()
                
                response = client.get(f"{API_URL}/recycling-points/", params=params)
                
                if response.status_code == 200:
                    points = response.json()
                    self.recycling_points = [RecyclingPoint(**p) for p in points]
        except Exception as e:
            print(f"Error cargando puntos: {e}")
        finally:
            self.loading = False
    
    def load_active_routes(self):
        """Cargar rutas activas"""
        try:
            with httpx.Client() as client:
                response = client.get(f"{API_URL}/routes/")
                
                if response.status_code == 200:
                    routes = response.json()
                    self.active_routes = [Route(**r) for r in routes]
        except Exception as e:
            print(f"Error cargando rutas: {e}")
    
    def load_gamification_stats(self):
        """Cargar estadísticas de gamificación"""
        if not self.token or not self.current_user:
            return
        
        try:
            with httpx.Client() as client:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = client.get(
                    f"{API_URL}/gamification/my-stats",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.gamification_stats = GamificationStats(**data)
                    
                    # Cargar leaderboard
                    self.load_leaderboard()
        except Exception as e:
            print(f"Error cargando stats: {e}")
    
    def load_leaderboard(self):
        """Cargar leaderboard"""
        try:
            with httpx.Client() as client:
                response = client.get(f"{API_URL}/gamification/leaderboard")
                
                if response.status_code == 200:
                    self.leaderboard = response.json()
        except Exception as e:
            print(f"Error cargando leaderboard: {e}")
    
    def load_my_collections(self):
        """Cargar mis colecciones"""
        if not self.token:
            return
        
        try:
            with httpx.Client() as client:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = client.get(
                    f"{API_URL}/collections/my-collections",
                    headers=headers
                )
                
                if response.status_code == 200:
                    collections = response.json()
                    self.my_collections = [Collection(**c) for c in collections]
        except Exception as e:
            print(f"Error cargando colecciones: {e}")
    
    def create_collection(self, waste_type: str, weight_kg: int = 1):
        """Crear nueva colección"""
        if not self.token:
            return
        
        self.loading = True
        try:
            with httpx.Client() as client:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = client.post(
                    f"{API_URL}/collections/",
                    headers=headers,
                    json={
                        "waste_type": waste_type,
                        "weight_kg": weight_kg,
                    }
                )
                
                if response.status_code == 200:
                    # Recargar datos
                    self.load_my_collections()
                    self.load_gamification_stats()
                    rx.toast("¡Colección creada! Ganaste puntos.", position="bottom")
        except Exception as e:
            rx.toast(f"Error: {str(e)}", position="bottom")
        finally:
            self.loading = False
