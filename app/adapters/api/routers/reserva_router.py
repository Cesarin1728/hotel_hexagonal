# router: para agrupar los endpoints relacionados con el mismo tema, en este caso las reservas. El router se encarga de recibir las solicitudes HTTP, llamar al servicio correspondiente y devolver la respuesta. No sabe nada de la BD, solo se comunica con el servicio.
# hace de adaptador
from fastapi import APIRouter, HTTPException, Depends # APIRouter es la clase que usamos para crear un router, HTTPException es para manejar errores y devolver respuestas con códigos HTTP
from app.adapters.api.schemas.reserva_schema import ReservaRequest, ReservaResponse
from app.application.services.reserva_service import ReservaService
from app.infrastructure.db.mysql.reserva_repo import PostgresReservaRepository # el repositorio concreto que implementa la interfaz ReservaRepository, en este caso para PostgreSQL (SupaBase)
from app.infrastructure.db.mysql.cuarto_repo import PostgresCuartoRepository
from app.infrastructure.db.mysql.huesped_repo import PostgresHuespedRepository
from app.adapters.api.dependencies.auth_deps import obtener_usuario_actual, requerir_admin

router = APIRouter(prefix="/api/reservas", tags=["Reservas"]) # prefix es el prefijo común para todas las rutas de este router, tags es para agruparlas en la documentación automática de FastAPI
service = ReservaService(PostgresReservaRepository(), PostgresCuartoRepository(), PostgresHuespedRepository()) # creamos una instancia del servicio, inyectándole el repositorio concreto que implementa la interfaz ReservaRepository. Esto es la inyección de dependencias manual

# Solo Administrador
# @router.get("/") registra este método como un endpoint GET en /api/reservas/
@router.get("/", response_model=list[ReservaResponse])
def listar(_=Depends(requerir_admin)):
    return service.list_reservas() # solo llama a service.list_reservas() y devuelve el resultado

# El huésped dueño o Administrador
@router.get("/{id}", response_model=ReservaResponse) # {id} es un parámetro de ruta, FastAPI lo convierte automáticamente a int porque lo definimos así en la función obtener(id: int)
def obtener(id: int, current_user: dict = Depends(obtener_usuario_actual)):
    r = service.get_reserva(id) # llama a service.get_reserva(id) para obtener la reserva con ese ID
    # si es none lanzamos la excepción HTTPException con código 404 (no encontrado) y un mensaje
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if current_user.get("rol") != "Administrador" and current_user.get("id") != r.id_huesped:
        raise HTTPException(status_code=403, detail="No puedes ver reservas de otros huéspedes")
        
    return r

# El propio huésped o Administrador
@router.get("/huesped/{id_huesped}", response_model=list[ReservaResponse])
def por_huesped(id_huesped: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador" and current_user.get("id") != id_huesped:
        raise HTTPException(status_code=403, detail="No puedes ver reservas de otro huésped")
    return service.get_reservas_por_huesped(id_huesped)

# Cualquier usuario autenticado
@router.post("/", response_model=ReservaResponse)
def crear(data: ReservaRequest, current_user: dict = Depends(obtener_usuario_actual)):
    # Evita que un Cliente (Huésped) cree reservas usando el ID de alguien más
    if current_user.get("rol") != "Administrador" and current_user.get("id") != data.id_huesped:
        raise HTTPException(status_code=403, detail="No puedes crear reservas a nombre de otro huésped")
        
    return service.create_reserva(data.espacio, data.fecha, data.servicio_cuarto, data.noches, data.id_cuarto, data.id_huesped)

# El huésped dueño o Administrador
@router.put("/{id}", response_model=ReservaResponse)
def actualizar(id: int, data: ReservaRequest, current_user: dict = Depends(obtener_usuario_actual)):
    r = service.get_reserva(id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
    if current_user.get("rol") != "Administrador" and current_user.get("id") != r.id_huesped:
        raise HTTPException(status_code=403, detail="No puedes modificar reservas de otros huéspedes")
        
    return service.update_reserva(id, data.espacio, data.fecha, data.servicio_cuarto, data.noches, data.id_cuarto, data.id_huesped)

# Solo Administrador
@router.delete("/{id}")
def eliminar(id: int, _=Depends(requerir_admin)):
    service.delete_reserva(id)
    return {"message": "Reserva eliminada correctamente"}