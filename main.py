# main.py
import asyncio
from fastapi import FastAPI
from app.api.routers import events
from app.db.database import init_db

app = FastAPI(title="Bugster API", version="1.0.0")

# Incluir el router de eventos
app.include_router(events.router, prefix="/api/v1")

# Hook de inicio para inicializar la base de datos
@app.on_event("startup")
async def on_startup():
    # Esperar unos segundos para asegurar que MongoDB esté listo
    await asyncio.sleep(5)
    await init_db()