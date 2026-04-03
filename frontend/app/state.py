"""
Estado Global de Reflex para EcoLink
Maneja autenticación, usuario actual, datos de rutas, puntos, etc.
"""
import reflex as rx
import requests
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
    
    # Navegación
    current_page: str = "login"  # "login" o "register"
    
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
    auth_success: str = ""
    
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
        self.auth_success = ""
    
    def go_to_login(self):
        """Navegar a login"""
        self.current_page = "login"
        self.reset_form()
    
    def go_to_register(self):
        """Navegar a registro"""
        self.current_page = "register"
        self.reset_form()
    
    def handle_login(self):
        """Manejar login"""
        self.loading = True
        self.auth_error = ""
        
        try:
            # Usar requests que es sincrónico y funciona mejor en Reflex
            response = requests.post(
                f"{API_URL}/auth/login",
                json={
                    "email": self.login_email,
                    "password": self.login_password,
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.is_authenticated = True
                
                # Parsear usuario
                user_data = data["user"]
                self.current_user = User(**user_data)
                
                self.reset_form()
            else:
                try:
                    error_data = response.json()
                    self.auth_error = error_data.get("detail", "Email o contraseña incorrectos")
                except:
                    self.auth_error = "Email o contraseña incorrectos"
        except requests.exceptions.Timeout:
            self.auth_error = "Error: La solicitud tardó demasiado. Verifica que el backend está corriendo."
        except requests.exceptions.ConnectionError:
            self.auth_error = "Error: No se puede conectar al backend. ¿Está corriendo en http://localhost:8000?"
        except Exception as e:
            self.auth_error = f"Error: {str(e)}"
        finally:
            self.loading = False
    
    def handle_register(self):
        """Manejar registro"""
        self.loading = True
        self.auth_error = ""
        self.auth_success = ""
        
        # Validaciones
        if not self.register_email or not self.register_password or not self.register_full_name:
            self.auth_error = "❌ Por favor completa todos los campos"
            self.loading = False
            return
        
        if self.register_password != self.register_confirm_password:
            self.auth_error = "❌ Las contraseñas no coinciden"
            self.loading = False
            return
        
        try:
            # Usar requests que es sincrónico y funciona mejor en Reflex
            response = requests.post(
                f"{API_URL}/auth/register",
                json={
                    "email": self.register_email,
                    "full_name": self.register_full_name,
                    "password": self.register_password,
                },
                timeout=10
            )
            
            if response.status_code == 200:
                # ✅ Registro exitoso
                self.auth_success = f"✅ ¡Registro exitoso! Bienvenido {self.register_full_name}.\nRedirigiendo a login..."
                
                # Redirigir a login después de 1.5 segundos
                import time
                time.sleep(1.5)
                self.go_to_login()
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", "Error en registro")
                    self.auth_error = f"❌ {error_msg}"
                except:
                    self.auth_error = "❌ Error en registro"
        except requests.exceptions.Timeout:
            self.auth_error = "❌ Error: La solicitud tardó demasiado. Verifica que el backend está corriendo."
        except requests.exceptions.ConnectionError:
            self.auth_error = "❌ Error: No se puede conectar al backend. ¿Está corriendo en http://localhost:8000?"
        except Exception as e:
            self.auth_error = f"❌ Error: {str(e)}"
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
        self.go_to_login()
    
    def load_recycling_points(self):
        """Cargar puntos de acopio"""
        self.loading = True
        try:
            params = {}
            if self.waste_type_filter:
                params["waste_type"] = self.waste_type_filter.lower()
            
            response = requests.get(f"{API_URL}/recycling-points/", params=params, timeout=10)
            
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
            response = requests.get(f"{API_URL}/routes/", timeout=10)
            
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
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{API_URL}/gamification/my-stats",
                headers=headers,
                timeout=10
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
            response = requests.get(f"{API_URL}/gamification/leaderboard", timeout=10)
            
            if response.status_code == 200:
                self.leaderboard = response.json()
        except Exception as e:
            print(f"Error cargando leaderboard: {e}")
    
    def load_my_collections(self):
        """Cargar mis colecciones"""
        if not self.token:
            return
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{API_URL}/collections/my-collections",
                headers=headers,
                timeout=10
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
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{API_URL}/collections/",
                headers=headers,
                json={
                    "waste_type": waste_type,
                    "weight_kg": weight_kg,
                },
                timeout=10
            )
            
            if response.status_code == 200:
                # Recargar datos
                self.load_my_collections()
                self.load_gamification_stats()
                rx.toast("¡Colección creada! Ganaste puntos.", position="bottom")
        except requests.exceptions.Timeout:
            rx.toast("Error: La solicitud tardó demasiado tiempo", position="bottom")
        except requests.exceptions.ConnectionError:
            rx.toast("Error: No se puede conectar al servidor", position="bottom")
        except Exception as e:
            rx.toast(f"Error: {str(e)}", position="bottom")
        finally:
            self.loading = False
