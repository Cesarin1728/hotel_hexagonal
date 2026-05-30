from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData
from datetime import datetime
from app.domain.models.message import MensajeChat
from app.domain.ports.mensaje_repository import MensajeRepository

engine = create_engine("mysql+pymysql://root:@localhost/hotel_local")
metadata = MetaData()

mensaje_table = Table(
    "mensaje_chat", metadata,
    Column("ID_Mensaje", Integer, primary_key=True, autoincrement=True),
    Column("ID_Cliente", Integer),
    Column("Emisor", String(50)),
    Column("Contenido", String(1000)),
    Column("Fecha", DateTime, default=datetime.now)
)

class PostgresMensajeRepository(MensajeRepository):
    def guardar(self, mensaje: MensajeChat) -> MensajeChat:
        with engine.connect() as conn:
            result = conn.execute(
                mensaje_table.insert().values(
                    ID_Cliente=mensaje.id_cliente,
                    Emisor=mensaje.emisor,
                    Contenido=mensaje.contenido,
                    Fecha=mensaje.fecha
                )
            )
            conn.commit()
            mensaje.id = result.inserted_primary_key[0]
            return mensaje

    def obtener_historial(self, id_cliente: int):
        with engine.connect() as conn:
            result = conn.execute(mensaje_table.select().where(mensaje_table.c.ID_Cliente == id_cliente).order_by(mensaje_table.c.Fecha.asc()))
            return [MensajeChat(id=row.ID_Mensaje, id_cliente=row.ID_Cliente, emisor=row.Emisor, contenido=row.Contenido, fecha=row.Fecha) for row in result]