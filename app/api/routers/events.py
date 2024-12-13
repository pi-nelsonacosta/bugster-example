# app/api/routers/events.py

from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.event import EventInput, UserStory, PlaywrightTest
from app.services.event_service import EventService
import subprocess
import os

router = APIRouter()
event_service = EventService()

@router.post("/events", summary="Recibe y almacena eventos - Genera Eventos, User Stories y Playwright Tests")
async def receive_events(payload: dict):
    try:
        events_data = payload.get("events", [])
        if not events_data:
            raise HTTPException(status_code=400, detail="No events provided")

        events = [EventInput(**event) for event in events_data]
        await event_service.store_events(events)
        return {"message": "Eventos recibidos correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stories", response_model=List[UserStory], summary="Obtiene historias de usuario")
async def get_stories(session_id: str = None):
    try:
        print(f"Recibida solicitud para session_id: {session_id}")
        stories = await event_service.get_user_stories(session_id)
        print(f"Historias devueltas: {stories}")
        return stories
    except Exception as e:
        print(f"Error en el endpoint /stories: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tests", response_model=List[PlaywrightTest], summary="Obtiene tests Playwright")
async def get_tests(story_id: str):
    try:
        tests = await event_service.get_tests_by_story_id(story_id)
        return tests
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/execute_test/{story_id}", summary="Ejecuta un test Playwright basado en el story_id")
async def execute_test(story_id: str):
    try:
        # 1. Recuperar el test desde la base de datos
        tests = await event_service.get_tests_by_story_id(story_id)
        if not tests:
            raise HTTPException(status_code=404, detail="No se encontró ningún test para el story_id proporcionado")

        test_script = tests[0].test_script  # Asumimos que hay al menos un test

        # 2. Guardar el script en un archivo temporal
        temp_test_file = f"/tmp/test_{story_id}.py"
        with open(temp_test_file, "w") as file:
            file.write(test_script)

        # 3. Ejecutar el script usando subprocess
        result = subprocess.run(
            ["pytest", temp_test_file],
            capture_output=True,
            text=True
        )

        # 4. Eliminar el archivo temporal después de la ejecución
        os.remove(temp_test_file)

        # 5. Devolver el resultado de la ejecución
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
