from sqlalchemy import create_engine, text
from typing import List, Optional
from app.domain.models.huesped import Huesped
from app.domain.ports.huesped_repository import HuespedRepository
from app.infrastructure.config.settings import DB_URL

engine = create_engine(DB_URL)

class PostgresHuespedRepository(HuespedRepository):

    def create(self, h: Huesped) -> Huesped:
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO "Huesped" ("Username", "Clave", "Miembro", "Economia", "Edad")
                VALUES (:username, :clave, :miembro, :economia, :edad)
                RETURNING "ID_Huesped"
            """), {"username": h.username, "clave": h.clave, "miembro": h.miembro, "economia": h.economia, "edad": h.edad})
            conn.commit()
            row = result.fetchone()
            h.id = row[0]
            return h

    def get_all(self) -> List[Huesped]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM "Huesped"'))
            return [Huesped(id=r[0], username=r[1], clave=r[2], miembro=r[3], economia=r[4], edad=r[5]) for r in result]

    def get_by_id(self, id: int) -> Optional[Huesped]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM "Huesped" WHERE "ID_Huesped" = :id'), {"id": id})
            r = result.fetchone()
            if r is None:
                return None
            return Huesped(id=r[0], username=r[1], clave=r[2], miembro=r[3], economia=r[4], edad=r[5])

    def update(self, id: int, h: Huesped) -> Huesped:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE "Huesped" SET "Username"=:username, "Clave"=:clave, "Miembro"=:miembro,
                "Economia"=:economia, "Edad"=:edad WHERE "ID_Huesped"=:id
            """), {"username": h.username, "clave": h.clave, "miembro": h.miembro, "economia": h.economia, "edad": h.edad, "id": id})
            conn.commit()
            return h

    def delete(self, id: int) -> None:
        with engine.connect() as conn:
            conn.execute(text('DELETE FROM "Huesped" WHERE "ID_Huesped" = :id'), {"id": id})
            conn.commit()