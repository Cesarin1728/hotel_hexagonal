from typing import List, Optional, BinaryIO
from app.domain.models.cuarto import Cuarto
from app.domain.ports.cuarto_repository import CuartoRepository
from app.domain.ports.storage_port import StoragePort

class CuartoService:
    def __init__(self, repository: CuartoRepository, storage: StoragePort):
        self.repository = repository
        self.storage = storage

    def create_cuarto(self, nombre: str, detalles: str, precio: int, espacio: str, file_stream: BinaryIO, filename: str, content_type: str) -> Cuarto:
        imagen_url = self.storage.upload_file(file_stream, filename, content_type)
        cuarto = Cuarto(id=None, nombre=nombre, detalles=detalles, precio=precio, espacio=espacio, imagen_url=imagen_url)
        return self.repository.create(cuarto)

    def list_cuartos(self) -> List[Cuarto]:
        return self.repository.get_all()

    def get_cuarto(self, id: int) -> Optional[Cuarto]:
        return self.repository.get_by_id(id)
    
    def update_cuarto(self, id: int, nombre: str, detalles: str, precio: int, espacio: str, file_stream=None, filename=None, content_type=None) -> Cuarto:
        cuarto_existente = self.repository.get_by_id(id)
        if not cuarto_existente:
            raise Exception("Cuarto no encontrado")
        
        # Mantenemos la imagen original si no suben una nueva
        imagen_url = cuarto_existente.imagen_url
        if file_stream:
            imagen_url = self.storage.upload_file(file_stream, filename, content_type)
            
        cuarto_actualizado = Cuarto(id=id, nombre=nombre, detalles=detalles, precio=precio, espacio=espacio, imagen_url=imagen_url)
        return self.repository.update(id, cuarto_actualizado)