from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.adapters.api.schemas.auth_schema import UserCreateRequest, TokenResponse, RefreshRequest, UsuarioResponse
from app.adapters.api.dependencies.auth_deps import obtener_usuario_actual
from app.application.services.auth_service import AuthService
from app.infrastructure.db.mysql.usuario_repo import MySQLUsuarioRepository
from app.infrastructure.db.mysql.huesped_repo import PostgresHuespedRepository
from app.infrastructure.security.bcrypt_hasher import BcryptAdapter
from app.infrastructure.security.jwt_manager import JWTManager

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

auth_service = AuthService(
    repository=MySQLUsuarioRepository(),
    hasher=BcryptAdapter(),
    jwt_manager=JWTManager()
)
huesped_repo = PostgresHuespedRepository()

@router.post("/register", response_model=UsuarioResponse)
def register(data: UserCreateRequest):
    u = auth_service.registrar_usuario(data.email, data.password, data.rol)
    return UsuarioResponse(id=u.id, email=u.email, rol=u.rol)

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_service.autenticar_usuario(form_data.username, form_data.password)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest):
    return auth_service.renovar_token(data.refresh_token)

@router.delete("/cuenta")
def eliminar_cuenta(current_user: dict = Depends(obtener_usuario_actual)):
    id_usuario = current_user.get("id")
    huespedes = huesped_repo.get_all()
    huesped = next((h for h in huespedes if h.id_usuario == id_usuario), None)
    if huesped:
        huesped_repo.delete(huesped.id)
    auth_service.repository.delete(id_usuario)
    return {"message": "Cuenta eliminada correctamente"}