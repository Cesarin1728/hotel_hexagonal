from fastapi import FastAPI
from app.adapters.api.routers.auth_router    import router as auth_router
from app.adapters.api.routers.cuarto_router  import router as cuarto_router
from app.adapters.api.routers.huesped_router import router as huesped_router
from app.adapters.api.routers.reserva_router import router as reserva_router
# Importar el nuevo router de WebSockets
from app.adapters.realtime.chat_router       import router as chat_router

app = FastAPI(
    title="Hotel API - Arquitectura Hexagonal + Auth",
    description="Usa /api/auth/login para obtener tu token y luego el botón Authorize arriba a la derecha.",
    version="2.0.0"
)

app.include_router(auth_router)
app.include_router(cuarto_router)
app.include_router(huesped_router)
app.include_router(reserva_router)
# Registrar el router del chat
app.include_router(chat_router)

# Poner en al terminal de la carpeta para ejecurar el proyecto al iniciar
# venv\Scripts\activate     
# uvicorn main:app --reload

# URL de FastAPI 
# http://127.0.0.1:8000/docs