# app/models/event.py

from typing import Dict
from pydantic import BaseModel, Field
from bson import ObjectId

# Modelo para el evento
class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    event: str
    properties: Dict
    timestamp: str

# Modelo para la historia de usuario
class UserStory(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    session_id: str
    journey_id: str
    description: str
