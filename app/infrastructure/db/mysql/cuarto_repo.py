from sqlalchemy import create_engine, text
from typing import List, Optional
from app.domain.models.cuarto import Cuarto
from app.domain.ports.cuarto_repository import CuartoRepository
from app.infrastructure.config.settings import DB_URL

engine = create_engine(DB_URL)

class PostgresCuartoRepository(CuartoRepository):

    def create(self, c: Cuarto) -> Cuarto:
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO "Cuarto" ("Nombre", "Detalles", "Precio", "Espacio")
                VALUES (:nombre, :detalles, :precio, :espacio)
                RETURNING "ID_Cuarto"
            """), {"nombre": c.nombre, "detalles": c.detalles, "precio": c.precio, "espacio": c.espacio})
            conn.commit()
            row = result.fetchone()
            c.id = row[0]
            return c

    def get_all(self) -> List[Cuarto]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM "Cuarto"'))
            return [Cuarto(id=r[0], nombre=r[1], detalles=r[2], precio=r[3], espacio=r[4]) for r in result]

    def get_by_id(self, id: int) -> Optional[Cuarto]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM "Cuarto" WHERE "ID_Cuarto" = :id'), {"id": id})
            r = result.fetchone()
            if r is None:
                return None
            return Cuarto(id=r[0], nombre=r[1], detalles=r[2], precio=r[3], espacio=r[4])

    def update(self, id: int, c: Cuarto) -> Cuarto:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE "Cuarto" SET "Nombre"=:nombre, "Detalles"=:detalles,
                "Precio"=:precio, "Espacio"=:espacio WHERE "ID_Cuarto"=:id
            """), {"nombre": c.nombre, "detalles": c.detalles, "precio": c.precio, "espacio": c.espacio, "id": id})
            conn.commit()
            return c

    def delete(self, id: int) -> None:
        with engine.connect() as conn:
            conn.execute(text('DELETE FROM "Cuarto" WHERE "ID_Cuarto" = :id'), {"id": id})
            conn.commit()