# app/repository/event_repository.py

from app.schemas.event import EventInput, UserStory
from app.db.database import event_collection, story_collection
from app.schemas.event import PlaywrightTest
from app.db.database import test_collection

from typing import List
from bson import ObjectId

# Almacenar eventos en MongoDB
async def store_events(events: List[EventInput]):
    try:
        print("Intentando almacenar eventos en MongoDB...")
        for event in events:
            print("Evento a almacenar:", event.dict(by_alias=True))
        result = await event_collection.insert_many([event.dict(by_alias=True) for event in events])
        print("Eventos almacenados correctamente, IDs:", result.inserted_ids)
    except Exception as e:
        print(f"Error al almacenar eventos: {e}")
        raise e

# Almacenar tests en MongoDB
async def store_tests(tests: List[PlaywrightTest]):
    await test_collection.insert_many([test.dict(by_alias=True) for test in tests])    

# Obtener eventos por session_id
async def get_events_by_session_id(session_id: str) -> List[EventInput]:
    try:
        print(f"Buscando eventos con session_id: {session_id}")
        events = await event_collection.find({"properties.session_id": session_id}).to_list(1000)
        print(f"Eventos encontrados: {events}")
        return [EventInput(**event) for event in events]
    except Exception as e:
        print(f"Error al obtener eventos por session_id ({session_id}): {e}")
        raise e

# Crear una historia de usuario
async def create_user_story(session_id: str, journey_id: str, description: str) -> UserStory:
    try:
        story = {
            "session_id": session_id,
            "journey_id": journey_id,
            "description": description
        }
        result = await story_collection.insert_one(story)
        
        # Asignar el _id de MongoDB como id en UserStory
        story["id"] = str(result.inserted_id)
        
        print(f"Historia insertada en MongoDB con ID: {story['id']}")
        return UserStory(**story)
    except Exception as e:
        print(f"Error al crear una historia: {e}")
        raise e

async def get_tests_by_story_id(story_id: str) -> List[PlaywrightTest]:
    """Recupera los tests de la base de datos filtrados por story_id."""
    try:
        cursor = test_collection.find({"story_id": story_id})
        tests = await cursor.to_list(length=None)
        return [PlaywrightTest(**test) for test in tests]
    except Exception as e:
        print(f"Error al obtener tests por story_id: {e}")
        raise e

async def get_stories_by_session_id(session_id: str) -> List[UserStory]:
    try:
        print(f"Buscando historias con session_id: {session_id}")
        cursor = story_collection.find({"session_id": session_id})
        stories = await cursor.to_list(1000)

        # Convertir _id a id
        for story in stories:
            story["id"] = str(story["_id"])
            del story["_id"]  # Eliminar el campo _id original

        print(f"Historias encontradas en MongoDB: {stories}")
        return [UserStory(**story) for story in stories]
    except Exception as e:
        print(f"Error al obtener historias por session_id ({session_id}): {e}")
        raise e
