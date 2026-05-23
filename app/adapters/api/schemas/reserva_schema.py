
from pydantic import BaseModel #BaseModel es la clase madre de todos los schemas, para definir cómo se ven los datos que entran y salen de la API (FastAPI). 
from datetime import datetime

# schema: para definir la forma de los datos que la API recibe (ReservaRequest) y envía (ReservaResponse). 
# el schema es la forma en que FastAPI valida y documenta los datos que recibe y envía. No sabe nada de la BD, solo define la estructura de los datos para la API.
class ReservaRequest(BaseModel):  # lo que la API recibe. Se calcula en la aplicación
    espacio: str
    fecha: datetime
    servicio_cuarto: bool
    noches: int
    id_cuarto: int
    id_huesped: int
 
class ReservaResponse(BaseModel):  # lo que la API envía
    id: int
    espacio: str
    fecha: datetime
    servicio_cuarto: bool
    noches: int
    costo: int
    id_cuarto: int
    id_huesped: int