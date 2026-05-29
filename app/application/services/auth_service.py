from app.domain.models.usuario import Usuario
from app.domain.ports.usuario_repository import UsuarioRepository
from app.domain.ports.password_hasher import PasswordHasher
from fastapi import HTTPException

class AuthService:
    def __init__(self, repository: UsuarioRepository, hasher: PasswordHasher, jwt_manager):
        self.repository  = repository
        self.hasher      = hasher
        self.jwt_manager = jwt_manager

    def registrar_usuario(self, email: str, password: str, rol: str = "Cliente") -> Usuario:
        if self.repository.get_by_email(email):
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        if rol not in ("Cliente", "Administrador"):
            raise HTTPException(status_code=422, detail="El rol debe ser 'Cliente' o 'Administrador'")

        nuevo = Usuario(id=None, email=email, password_hash=self.hasher.hash(password), rol=rol)
        return self.repository.create(nuevo)

    def autenticar_usuario(self, email: str, password: str) -> dict:
        usuario = self.repository.get_by_email(email)
        if not usuario or not self.hasher.verify(password, usuario.password_hash):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        access_token  = self.jwt_manager.create_access_token({"sub": usuario.email, "rol": usuario.rol, "id":  usuario.id})
        refresh_token = self.jwt_manager.create_refresh_token({"sub": usuario.email})

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    def renovar_token(self, refresh_token: str) -> dict:
        payload = self.jwt_manager.decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")

        usuario = self.repository.get_by_email(payload.get("sub"))
        if not usuario:
            raise HTTPException(status_code=404, detail="El usuario ya no existe")

        nuevo_access = self.jwt_manager.create_access_token({"sub": usuario.email, "rol": usuario.rol, "id":  usuario.id})
        return {"access_token": nuevo_access, "token_type": "bearer"}