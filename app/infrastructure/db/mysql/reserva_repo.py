# La infraestructura. Es la parte que se conecta con el exterior, en este caso con Supabase (PostgreSQL).
# Aquí se implementan los contratos de nuestro puerto, en este caso de ReservaRepository
from sqlalchemy import create_engine, text
from typing import List, Optional
from app.domain.models.reserva import Reserva
from app.domain.ports.reserva_repository import ReservaRepository
from app.infrastructure.config.settings import DB_URL

engine = create_engine(DB_URL)

class PostgresReservaRepository(ReservaRepository):

    def create(self, r: Reserva) -> Reserva:
        with engine.connect() as conn:
            conn.execute(text(""" 
                INSERT INTO `Reserva` (`Espacio`, `Fecha`, `ServicioCuarto`, `Noches`, `ID_Cuarto`, `ID_Huesped`)
                VALUES (:espacio, :fecha, :servicio_cuarto, :noches, :id_cuarto, :id_huesped)
            """), {"espacio": r.espacio, "fecha": r.fecha, "servicio_cuarto": r.servicio_cuarto, 
                  "noches": r.noches, "id_cuarto": r.id_cuarto, "id_huesped": r.id_huesped})
            
            result_id = conn.execute(text("SELECT LAST_INSERT_ID()"))
            row_id = result_id.fetchone()
            conn.commit()
            
            r.id = row_id[0]
            return r

    def get_all(self) -> List[Reserva]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM `Reserva`'))
            return [
                Reserva(
                    id=row._mapping["ID_Reserva"],
                    espacio=row._mapping["Espacio"],
                    fecha=row._mapping["Fecha"],
                    servicio_cuarto=row._mapping["ServicioCuarto"],
                    noches=row._mapping["Noches"],
                    id_cuarto=row._mapping["ID_Cuarto"],
                    id_huesped=row._mapping["ID_Huesped"]
                ) for row in result
            ]

    def get_by_id(self, id: int) -> Optional[Reserva]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM `Reserva` WHERE `ID_Reserva` = :id'), {"id": id})
            r = result.fetchone()
            if r is None:
                return None
            return Reserva(
                id=r._mapping["ID_Reserva"],
                espacio=r._mapping["Espacio"],
                fecha=r._mapping["Fecha"],
                servicio_cuarto=r._mapping["ServicioCuarto"],
                noches=r._mapping["Noches"],
                id_cuarto=r._mapping["ID_Cuarto"],
                id_huesped=r._mapping["ID_Huesped"]
            )

    def get_by_huesped(self, id_huesped: int) -> List[Reserva]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM `Reserva` WHERE `ID_Huesped` = :id'), {"id": id_huesped})
            return [
                Reserva(
                    id=row._mapping["ID_Reserva"],
                    espacio=row._mapping["Espacio"],
                    fecha=row._mapping["Fecha"],
                    servicio_cuarto=row._mapping["ServicioCuarto"],
                    noches=row._mapping["Noches"],
                    id_cuarto=row._mapping["ID_Cuarto"],
                    id_huesped=row._mapping["ID_Huesped"]
                ) for row in result
            ]

    def update(self, id: int, r: Reserva) -> Reserva:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE `Reserva` SET `Espacio`=:espacio, `Fecha`=:fecha, `ServicioCuarto`=:servicio_cuarto,
                `Noches`=:noches, `ID_Cuarto`=:id_cuarto, `ID_Huesped`=:id_huesped
                WHERE `ID_Reserva`=:id
            """), {"espacio": r.espacio, "fecha": r.fecha, "servicio_cuarto": r.servicio_cuarto,
                  "noches": r.noches, "id_cuarto": r.id_cuarto, "id_huesped": r.id_huesped, "id": id})
            conn.commit()
            return r

    def delete(self, id: int) -> None:
        with engine.connect() as conn:
            conn.execute(text('DELETE FROM `Reserva` WHERE `ID_Reserva` = :id'), {"id": id})
            conn.commit()