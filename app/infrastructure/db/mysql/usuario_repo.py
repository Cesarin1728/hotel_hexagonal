from sqlalchemy import text
from typing import Optional
from app.domain.models.usuario import Usuario
from app.domain.ports.usuario_repository import UsuarioRepository
from app.infrastructure.config.settings import engine

class MySQLUsuarioRepository(UsuarioRepository):
    def create(self, u: Usuario) -> Usuario:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO `Usuario` (`Email`, `PasswordHash`, `Rol`)
                VALUES (:email, :password_hash, :rol)
            """), {"email": u.email, "password_hash": u.password_hash, "rol": u.rol})
            result_id = conn.execute(text("SELECT LAST_INSERT_ID()"))
            u.id = result_id.fetchone()[0]
            conn.commit()
            return u

    def get_by_email(self, email: str) -> Optional[Usuario]:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM `Usuario` WHERE `Email` = :email"),
                {"email": email}
            )
            row = result.fetchone()
            if not row:
                return None
            m = row._mapping
            return Usuario(
                id=m["ID_Usuario"], email=m["Email"],
                password_hash=m["PasswordHash"], rol=m["Rol"]
            )