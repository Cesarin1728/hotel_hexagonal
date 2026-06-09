from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.adapters.api.routers import cuarto_router, auth_router, huesped_router, reserva_router
from app.adapters.realtime import chat_router

app = FastAPI(title="Hotel Hexagonal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(cuarto_router.router)
app.include_router(huesped_router.router)
app.include_router(reserva_router.router)
app.include_router(chat_router.router)

# Poner en al terminal de la carpeta para ejecurar el proyecto al iniciar
# venv\Scripts\activate     
# uvicorn main:app --reload

# URL de FastAPI 
# http://127.0.0.1:8000/docs
