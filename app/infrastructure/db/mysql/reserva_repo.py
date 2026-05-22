# La infraestructura. Es la parte que se conecta con el exterior, en este caso con Supabase (PostgreSQL).
# Aquí se implementan los contratos de nuestro puerto, en este caso de ReservaRepository
from sqlalchemy import create_engine, text #Libreríá externa para manejar la conexión a la base de datos y ejecutar consultas SQL
from typing import List, Optional
from app.domain.models.reserva import Reserva
from app.domain.ports.reserva_repository import ReservaRepository
from app.infrastructure.config.settings import DB_URL # importar la URL de conexión (la sacamos de SupaBase)

engine = create_engine(DB_URL) # engine es de SQLAlchemy. Es el objeto que maneja la conexión con Supabase (PostgreSQl)

class PostgresReservaRepository(ReservaRepository): #Hereda de ReservaRepository, por lo tanto debe implementar todos sus métodos

    def create(self, r: Reserva) -> Reserva:
        #with es para manejar recursos de forma segura, en este caso la conexión a la base de datos. Se asegura de que se cierre correctamente después de usarla, también si ocurre un error.
        with engine.connect() as conn: # se abre una conexión pool con la BD, se cierra al salir del with. "Una conexión pool es un conjunto de conexiones preestablecidas que se reutilizan para mejorar el rendimiento"
            #text es una función de SQLAlchemy que permite escribir consultas SQL como texto
            result = conn.execute(text(""" 
                INSERT INTO "Reserva" ("Espacio", "Fecha", "ServicioCuarto", "Noches", "ID_Cuarto", "ID_Huesped")
                VALUES (:espacio, :fecha, :servicio_cuarto, :noches, :id_cuarto, :id_huesped)
                RETURNING "ID_Reserva"
            """), {"espacio": r.espacio, "fecha": r.fecha, "servicio_cuarto": r.servicio_cuarto, 
                  "noches": r.noches, "id_cuarto": r.id_cuarto, "id_huesped": r.id_huesped})
            conn.commit() # confirma la transacción, sin esto el INSERT no se guarda
            row = result.fetchone() # obtiene la fila devuelta por RETURNING (ID_Reserva)
            r.id = row[0] # guarda el ID asignado por la BD en la inatancia de Reserva
            return r # devuelve la reserva con el ID

    def get_all(self) -> List[Reserva]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM "Reserva"'))
            # r[] es cada fila del resultado, r[0] es ID_Reserva, r[1] es Espacio, etc. El índice del corchete es en base al orden de las columnas en la tabla.
            # el for recorre todas las filas del resultado y crea una instancia de Reserva por cada una (las guardamos en la lista), luego devuelve la lista completa de reservas
            return [Reserva(id=r[0], espacio=r[1], fecha=r[2], servicio_cuarto=r[3], noches=r[4], id_cuarto=r[5], id_huesped=r[6]) for r in result]

    def get_by_id(self, id: int) -> Optional[Reserva]: # devuelve una reserva específica por su ID, o None si no existe (gracias al Optional). 
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM "Reserva" WHERE "ID_Reserva" = :id'), {"id": id})
            r = result.fetchone() #fetchone() devuelve solo una fila
            if r is None:
                return None
            return Reserva(id=r[0], espacio=r[1], fecha=r[2], servicio_cuarto=r[3], noches=r[4], id_cuarto=r[5], id_huesped=r[6])

    def get_by_huesped(self, id_huesped: int) -> List[Reserva]:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM "Reserva" WHERE "ID_Huesped" = :id'), {"id": id_huesped})
            return [Reserva(id=r[0], espacio=r[1], fecha=r[2], servicio_cuarto=r[3], noches=r[4], id_cuarto=r[5], id_huesped=r[6]) for r in result]

    def update(self, id: int, r: Reserva) -> Reserva:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE "Reserva" SET "Espacio"=:espacio, "Fecha"=:fecha, "ServicioCuarto"=:servicio_cuarto,
                "Noches"=:noches, "ID_Cuarto"=:id_cuarto, "ID_Huesped"=:id_huesped
                WHERE "ID_Reserva"=:id
            """), {"espacio": r.espacio, "fecha": r.fecha, "servicio_cuarto": r.servicio_cuarto,
                  "noches": r.noches, "id_cuarto": r.id_cuarto, "id_huesped": r.id_huesped, "id": id})
            conn.commit()
            return r

    def delete(self, id: int) -> None:
        with engine.connect() as conn:
            conn.execute(text('DELETE FROM "Reserva" WHERE "ID_Reserva" = :id'), {"id": id})
            conn.commit()