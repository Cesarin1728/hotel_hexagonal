from fastapi import APIRouter, HTTPException
from app.adapters.api.schemas.huesped_schema import HuespedRequest, HuespedResponse
from app.application.services.huesped_service import HuespedService
from app.infrastructure.db.mysql.huesped_repo import PostgresHuespedRepository

router = APIRouter(prefix="/api/huespedes", tags=["Huéspedes"])
service = HuespedService(PostgresHuespedRepository())

@router.get("/", response_model=list[HuespedResponse])
def listar():
    return service.list_huespedes()

@router.get("/{id}", response_model=HuespedResponse)
def obtener(id: int):
    h = service.get_huesped(id)
    if not h:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")
    return h

@router.post("/", response_model=HuespedResponse)
def crear(data: HuespedRequest):
    return service.create_huesped(data.username, data.clave, data.miembro, data.economia, data.edad)

@router.put("/{id}", response_model=HuespedResponse)
def actualizar(id: int, data: HuespedRequest):
    return service.update_huesped(id, data.username, data.clave, data.miembro, data.economia, data.edad)

@router.delete("/{id}")
def eliminar(id: int):
    service.delete_huesped(id)
    return {"message": "Huésped eliminado correctamente"}