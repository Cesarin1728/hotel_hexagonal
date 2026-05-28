from fastapi import FastAPI # FastAPI es el framework que usamos para crear la API RESTful. Nos permite definir endpoints, manejar solicitudes y respuestas, validar datos, generar documentación automática, etc.
from app.adapters.api.routers.huesped_router import router as huesped_router
from app.adapters.api.routers.cuarto_router import router as cuarto_router
from app.adapters.api.routers.reserva_router import router as reserva_router

app = FastAPI(
    title="Hotel API - Arquitectura Hexagonal",
    description="API RESTful para gestión de huéspedes, cuartos y reservas",
    version="1.0.0"
)

app.include_router(huesped_router)
app.include_router(cuarto_router)
app.include_router(reserva_router)

# Poner en al terminal de la carpeta para ejecurar el proyecto al iniciar
# venv\Scripts\activate     uvicorn main:app --reload

# URL de FastAPI 
# http://127.0.0.1:8000/docs