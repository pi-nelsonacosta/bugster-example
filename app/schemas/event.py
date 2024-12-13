# app/schemas/event.py

from pydantic import BaseModel, Field
from typing import Dict, List

class EventInput(BaseModel):
    event: str
    properties: Dict
    timestamp: str

class EventsPayload(BaseModel):
    events: List[EventInput]    

class UserStory(BaseModel):
    id: str
    session_id: str
    journey_id: str
    description: str

class PlaywrightTest(BaseModel):
    story_id: str
    test_script: str
