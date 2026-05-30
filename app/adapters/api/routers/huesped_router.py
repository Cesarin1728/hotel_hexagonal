from fastapi import APIRouter, HTTPException, Depends
from app.adapters.api.schemas.huesped_schema import HuespedRequest, HuespedResponse
from app.application.services.huesped_service import HuespedService
from app.infrastructure.db.mysql.huesped_repo import PostgresHuespedRepository
from app.adapters.api.dependencies.auth_deps import obtener_usuario_actual, requerir_admin

router  = APIRouter(prefix="/api/huespedes", tags=["Huéspedes"])
service = HuespedService(PostgresHuespedRepository())

# Solo Administrador
@router.get("/", response_model=list[HuespedResponse])
def listar(_=Depends(requerir_admin)):
    return service.list_huespedes()

# El propio huésped o Administrador
@router.get("/{id}", response_model=HuespedResponse)
def obtener(id: int, current_user: dict = Depends(obtener_usuario_actual)):
    h = service.get_huesped(id)
    if not h:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")
    
    # Seguridad: Comparamos el ID del token con el id_usuario dueño del perfil
    if current_user.get("rol") != "Administrador" and current_user.get("id") != h.id_usuario:
        raise HTTPException(status_code=403, detail="No puedes ver el perfil de otro huésped")
    return h

# Solo autenticados: el id_usuario se inyecta desde el token (Robo de identidad bloqueado)
@router.post("/", response_model=HuespedResponse)
def crear(data: HuespedRequest, current_user: dict = Depends(obtener_usuario_actual)):
    id_del_token = current_user.get("id")
    return service.create_huesped(id_del_token, data.username, data.clave, data.miembro, data.economia, data.edad)

# El propio huésped o Administrador
@router.put("/{id}", response_model=HuespedResponse)
def actualizar(id: int, data: HuespedRequest, current_user: dict = Depends(obtener_usuario_actual)):
    # Primero buscamos al huésped para saber quién es el dueño
    h = service.get_huesped(id)
    if not h:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")
        
    # Seguridad: Comparamos el ID del token con el id_usuario dueño del perfil
    if current_user.get("rol") != "Administrador" and current_user.get("id") != h.id_usuario:
        raise HTTPException(status_code=403, detail="No puedes modificar el perfil de otro huésped")
        
    return service.update_huesped(id, data.username, data.clave, data.miembro, data.economia, data.edad)

# Solo Administrador
@router.delete("/{id}")
def eliminar(id: int, _=Depends(requerir_admin)):
    service.delete_huesped(id)
    return {"message": "Huésped eliminado correctamente"}