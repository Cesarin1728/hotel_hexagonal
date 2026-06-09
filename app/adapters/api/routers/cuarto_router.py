from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from typing import Optional
from app.adapters.api.schemas.cuarto_schema import CuartoResponse
from app.application.services.cuarto_service import CuartoService
from app.infrastructure.db.mysql.cuarto_repo import PostgresCuartoRepository
from app.infrastructure.storage.s3_adapter import S3StorageAdapter
from app.adapters.api.dependencies.auth_deps import requerir_admin

router = APIRouter(prefix="/api/cuartos", tags=["Cuartos"])
service = CuartoService(PostgresCuartoRepository(), S3StorageAdapter())

@router.get("/", response_model=list[CuartoResponse])
def listar():
    return service.list_cuartos()

@router.post("/", response_model=CuartoResponse)
def crear(
    nombre: str = Form(...), 
    detalles: str = Form(...),
    precio: str = Form(...),
    espacio: str = Form(...),
    imagen: UploadFile = File(...),
    _=Depends(requerir_admin)
):
    try:
        # Convertimos explícitamente a int
        return service.create_cuarto(
            nombre=nombre, detalles=detalles, precio=int(precio), espacio=espacio,
            file_stream=imagen.file, filename=imagen.filename, content_type=imagen.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear: {str(e)}")

@router.put("/{id}", response_model=CuartoResponse)
def actualizar(
    id: int,
    nombre: str = Form(...), 
    detalles: str = Form(...),
    precio: str = Form(...), 
    espacio: str = Form(...),
    imagen: Optional[UploadFile] = File(None),
    _=Depends(requerir_admin)
):
    try:
        file_stream = imagen.file if imagen else None
        filename = imagen.filename if imagen else None
        content_type = imagen.content_type if imagen else None
        
        return service.update_cuarto(
            id=id, nombre=nombre, detalles=detalles, precio=int(precio), espacio=espacio,
            file_stream=file_stream, filename=filename, content_type=content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")

@router.delete("/{id}")
def eliminar(id: int, _=Depends(requerir_admin)):
    try:
        service.repository.delete(id)
        return {"message": "Cuarto eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))