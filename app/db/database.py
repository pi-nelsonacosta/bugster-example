from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017/bugster_db")
client = AsyncIOMotorClient(MONGO_URL)
database = client["bugster_db"]
event_collection = database["events"]
story_collection = database["stories"]
test_collection = database["tests"] 


async def init_db():
    """Elimina y recrea las colecciones vacías al iniciar la aplicación."""
    try:
        # Eliminar las colecciones si existen
        await event_collection.drop()
        await story_collection.drop()
        await test_collection.drop()
        print("Colecciones eliminadas correctamente.")

        # Re-crear las colecciones vacías
        await database.create_collection("events")
        await database.create_collection("stories")
        await database.create_collection("tests")
        print("Colecciones creadas nuevamente.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")