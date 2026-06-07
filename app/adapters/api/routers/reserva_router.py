from fastapi import APIRouter, HTTPException, Depends
from app.adapters.api.schemas.reserva_schema import ReservaRequest, ReservaResponse
from app.application.services.reserva_service import ReservaService
from app.infrastructure.db.mysql.reserva_repo import PostgresReservaRepository
from app.infrastructure.db.mysql.cuarto_repo import PostgresCuartoRepository
from app.infrastructure.db.mysql.huesped_repo import PostgresHuespedRepository
from app.adapters.api.dependencies.auth_deps import obtener_usuario_actual, requerir_admin

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])
service = ReservaService(PostgresReservaRepository(), PostgresCuartoRepository(), PostgresHuespedRepository())
huesped_repo = PostgresHuespedRepository()

def _resolver_id_huesped(id_usuario: int) -> int:
    """Convierte ID_Usuario → ID_Huesped. Lanza 404 si no existe perfil de huésped."""
    todos = huesped_repo.get_all()
    huesped = next((h for h in todos if h.id_usuario == id_usuario), None)
    if not huesped:
        raise HTTPException(status_code=404, detail="No tienes un perfil de huésped registrado")
    return huesped.id

@router.get("/", response_model=list[ReservaResponse])
def listar(_=Depends(requerir_admin)):
    return service.list_reservas()

@router.get("/huesped/{id_usuario}", response_model=list[ReservaResponse])
def por_huesped(id_usuario: int, current_user: dict = Depends(obtener_usuario_actual)):
    # Verificar que solo vea sus propias reservas
    if current_user.get("rol") != "Administrador" and current_user.get("id") != id_usuario:
        raise HTTPException(status_code=403, detail="No puedes ver reservas de otro huésped")
    # Convertir id_usuario → id_huesped real
    id_huesped = _resolver_id_huesped(id_usuario)
    return service.get_reservas_por_huesped(id_huesped)

@router.get("/{id}", response_model=ReservaResponse)
def obtener(id: int, current_user: dict = Depends(obtener_usuario_actual)):
    r = service.get_reserva(id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if current_user.get("rol") != "Administrador":
        id_huesped = _resolver_id_huesped(current_user.get("id"))
        if id_huesped != r.id_huesped:
            raise HTTPException(status_code=403, detail="No puedes ver reservas de otros huéspedes")
    return r

@router.post("/", response_model=ReservaResponse)
def crear(data: ReservaRequest, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        id_huesped_real = _resolver_id_huesped(current_user.get("id"))
        data.id_huesped = id_huesped_real
    return service.create_reserva(
        data.espacio, data.fecha, data.servicio_cuarto,
        data.noches, data.id_cuarto, data.id_huesped
    )

@router.put("/{id}", response_model=ReservaResponse)
def actualizar(id: int, data: ReservaRequest, current_user: dict = Depends(obtener_usuario_actual)):
    r = service.get_reserva(id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if current_user.get("rol") != "Administrador":
        id_huesped_real = _resolver_id_huesped(current_user.get("id"))
        if id_huesped_real != r.id_huesped:
            raise HTTPException(status_code=403, detail="No puedes modificar reservas de otros huéspedes")
    return service.update_reserva(
        id, data.espacio, data.fecha, data.servicio_cuarto,
        data.noches, data.id_cuarto, data.id_huesped
    )

@router.delete("/{id}")
def eliminar(id: int, current_user: dict = Depends(obtener_usuario_actual)):
    r = service.get_reserva(id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if current_user.get("rol") != "Administrador":
        id_huesped_real = _resolver_id_huesped(current_user.get("id"))
        if id_huesped_real != r.id_huesped:
            raise HTTPException(status_code=403, detail="No puedes eliminar reservas de otros huéspedes")
    service.delete_reserva(id)
    return {"message": "Reserva eliminada correctamente"}