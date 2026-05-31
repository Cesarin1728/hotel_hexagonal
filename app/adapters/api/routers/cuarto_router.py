from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
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
    nombre: str = Form(...), detalles: str = Form(...),
    precio: int = Form(...), espacio: str = Form(...),
    imagen: UploadFile = File(...),
    _=Depends(requerir_admin)
):
    try:
        return service.create_cuarto(
            nombre=nombre, detalles=detalles, precio=precio, espacio=espacio,
            file_stream=imagen.file, filename=imagen.filename, content_type=imagen.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))