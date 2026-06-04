from fastapi import APIRouter, HTTPException, Depends
from app.adapters.api.schemas.reserva_schema import ReservaRequest, ReservaResponse
from app.application.services.reserva_service import ReservaService
from app.infrastructure.db.mysql.reserva_repo import PostgresReservaRepository
from app.infrastructure.db.mysql.cuarto_repo import PostgresCuartoRepository
from app.infrastructure.db.mysql.huesped_repo import PostgresHuespedRepository
from app.adapters.api.dependencies.auth_deps import obtener_usuario_actual, requerir_admin

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])
service = ReservaService(PostgresReservaRepository(), PostgresCuartoRepository(), PostgresHuespedRepository())

@router.get("/", response_model=list[ReservaResponse])
def listar(_=Depends(requerir_admin)):
    return service.list_reservas()

@router.get("/{id}", response_model=ReservaResponse)
def obtener(id: int, current_user: dict = Depends(obtener_usuario_actual)):
    r = service.get_reserva(id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if current_user.get("rol") != "Administrador" and current_user.get("id") != r.id_huesped:
        raise HTTPException(status_code=403, detail="No puedes ver reservas de otros huéspedes")
    return r

@router.get("/huesped/{id_huesped}", response_model=list[ReservaResponse])
def por_huesped(id_huesped: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador" and current_user.get("id") != id_huesped:
        raise HTTPException(status_code=403, detail="No puedes ver reservas de otro huésped")
    return service.get_reservas_por_huesped(id_huesped)

@router.post("/", response_model=ReservaResponse)
def crear(data: ReservaRequest, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador" and current_user.get("id") != data.id_huesped:
        raise HTTPException(status_code=403, detail="No puedes crear reservas a nombre de otro huésped")
    return service.create_reserva(data.espacio, data.fecha, data.servicio_cuarto, data.noches, data.id_cuarto, data.id_huesped)

@router.put("/{id}", response_model=ReservaResponse)
def actualizar(id: int, data: ReservaRequest, current_user: dict = Depends(obtener_usuario_actual)):
    r = service.get_reserva(id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if current_user.get("rol") != "Administrador" and current_user.get("id") != r.id_huesped:
        raise HTTPException(status_code=403, detail="No puedes modificar reservas de otros huéspedes")
    return service.update_reserva(id, data.espacio, data.fecha, data.servicio_cuarto, data.noches, data.id_cuarto, data.id_huesped)

# ← CAMBIO: huésped dueño O administrador pueden eliminar
@router.delete("/{id}")
def eliminar(id: int, current_user: dict = Depends(obtener_usuario_actual)):
    r = service.get_reserva(id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if current_user.get("rol") != "Administrador" and current_user.get("id") != r.id_huesped:
        raise HTTPException(status_code=403, detail="No puedes eliminar reservas de otros huéspedes")
    service.delete_reserva(id)
    return {"message": "Reserva eliminada correctamente"}