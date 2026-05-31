from sqlalchemy import create_engine, text
from typing import List, Optional
from app.domain.models.huesped import Huesped
from app.domain.ports.huesped_repository import HuespedRepository
from app.infrastructure.config.settings import DB_URL

engine = create_engine(DB_URL)

class PostgresHuespedRepository(HuespedRepository):

    def create(self, h: Huesped) -> Huesped:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO `huesped` (`ID_Usuario`, `Username`, `Clave`, `Miembro`, `Economia`, `Edad`)
                VALUES (:id_usuario, :username, :clave, :miembro, :economia, :edad)
            """), {
                "id_usuario": h.id_usuario, 
                "username": h.username, 
                "clave": h.clave, 
                "miembro": h.miembro, 
                "economia": h.economia, 
                "edad": h.edad
            })
            conn.commit()
            
            result = conn.execute(text("SELECT LAST_INSERT_ID()"))
            h.id = result.scalar()
            return h

    def get_all(self) -> List[Huesped]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM `Huesped`'))
            return [
                Huesped(
                    id=row._mapping["ID_Huesped"],
                    id_usuario=row._mapping["ID_Usuario"], # <-- Corrección aquí
                    username=row._mapping["Username"],
                    clave=row._mapping["Clave"],
                    miembro=row._mapping["Miembro"],
                    economia=row._mapping["Economia"],
                    edad=row._mapping["Edad"]
                ) for row in result
            ]

    def get_by_id(self, id: int) -> Optional[Huesped]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM `Huesped` WHERE `ID_Huesped` = :id'), {"id": id})
            r = result.fetchone()
            if r is None:
                return None
            return Huesped(
                id=r._mapping["ID_Huesped"],
                id_usuario=r._mapping["ID_Usuario"], # <-- Corrección aquí
                username=r._mapping["Username"],
                clave=r._mapping["Clave"],
                miembro=r._mapping["Miembro"],
                economia=r._mapping["Economia"],
                edad=r._mapping["Edad"]
            )

    def update(self, id: int, h: Huesped) -> Huesped:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE `Huesped` SET `Username`=:username, `Clave`=:clave, `Miembro`=:miembro,
                `Economia`=:economia, `Edad`=:edad WHERE `ID_Huesped`=:id
            """), {"username": h.username, "clave": h.clave, "miembro": h.miembro, "economia": h.economia, "edad": h.edad, "id": id})
            conn.commit()
            return h

    def delete(self, id: int) -> None:
        with engine.connect() as conn:
            conn.execute(text('DELETE FROM `Huesped` WHERE `ID_Huesped` = :id'), {"id": id})
            conn.commit()