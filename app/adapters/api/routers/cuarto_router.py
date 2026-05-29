from fastapi import APIRouter, HTTPException, Depends
from app.adapters.api.schemas.cuarto_schema import CuartoRequest, CuartoResponse
from app.application.services.cuarto_service import CuartoService
from app.infrastructure.db.mysql.cuarto_repo import PostgresCuartoRepository
from app.adapters.api.dependencies.auth_deps import requerir_admin

router  = APIRouter(prefix="/api/cuartos", tags=["Cuartos"])
service = CuartoService(PostgresCuartoRepository())

# Público: cualquiera puede ver cuartos
@router.get("/", response_model=list[CuartoResponse])
def listar():
    return service.list_cuartos()

@router.get("/{id}", response_model=CuartoResponse)
def obtener(id: int):
    c = service.get_cuarto(id)
    if not c:
        raise HTTPException(status_code=404, detail="Cuarto no encontrado")
    return c

# Solo Administrador
@router.post("/", response_model=CuartoResponse)
def crear(data: CuartoRequest, _=Depends(requerir_admin)):
    return service.create_cuarto(data.nombre, data.detalles, data.precio, data.espacio)

@router.put("/{id}", response_model=CuartoResponse)
def actualizar(id: int, data: CuartoRequest, _=Depends(requerir_admin)):
    return service.update_cuarto(id, data.nombre, data.detalles, data.precio, data.espacio)

@router.delete("/{id}")
def eliminar(id: int, _=Depends(requerir_admin)):
    service.delete_cuarto(id)
    return {"message": "Cuarto eliminado correctamente"}