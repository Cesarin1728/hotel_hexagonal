from sqlalchemy import create_engine, text
from typing import List, Optional
from app.domain.models.cuarto import Cuarto
from app.domain.ports.cuarto_repository import CuartoRepository
from app.infrastructure.config.settings import DB_URL

engine = create_engine(DB_URL)

class PostgresCuartoRepository(CuartoRepository):

    def create(self, c: Cuarto) -> Cuarto:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO `Cuarto` (`Nombre`, `Detalles`, `Precio`, `Espacio`)
                VALUES (:nombre, :detalles, :precio, :espacio)
            """), {"nombre": c.nombre, "detalles": c.detalles, "precio": c.precio, "espacio": c.espacio})
            
            result_id = conn.execute(text("SELECT LAST_INSERT_ID()"))
            row_id = result_id.fetchone()
            conn.commit()
            
            c.id = row_id[0]
            return c

    def get_all(self) -> List[Cuarto]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM `Cuarto`'))
            return [
                Cuarto(
                    id=row._mapping["ID_Cuarto"],
                    nombre=row._mapping["Nombre"],
                    detalles=row._mapping["Detalles"],
                    precio=row._mapping["Precio"],
                    espacio=row._mapping["Espacio"]
                ) for row in result
            ]

    def get_by_id(self, id: int) -> Optional[Cuarto]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM `Cuarto` WHERE `ID_Cuarto` = :id'), {"id": id})
            r = result.fetchone()
            if r is None:
                return None
            return Cuarto(
                id=r._mapping["ID_Cuarto"],
                nombre=r._mapping["Nombre"],
                detalles=r._mapping["Detalles"],
                precio=r._mapping["Precio"],
                espacio=r._mapping["Espacio"]
            )

    def update(self, id: int, c: Cuarto) -> Cuarto:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE `Cuarto` SET `Nombre`=:nombre, `Detalles`=:detalles,
                `Precio`=:precio, `Espacio`=:espacio WHERE `ID_Cuarto`=:id
            """), {"nombre": c.nombre, "detalles": c.detalles, "precio": c.precio, "espacio": c.espacio, "id": id})
            conn.commit()
            return c

    def delete(self, id: int) -> None:
        with engine.connect() as conn:
            conn.execute(text('DELETE FROM `Cuarto` WHERE `ID_Cuarto` = :id'), {"id": id})
            conn.commit()