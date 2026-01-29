import json
from typing import List, Union
from http import HTTPStatus
from fastapi import APIRouter, Query, Path
from pydantic import BaseModel
from starlette.responses import Response

router = APIRouter()

# In-memory store for practice
EVENT_STORE = []

# -------------------------------
# Schemas
# -------------------------------
class EventSchema(BaseModel):
    """Event Schema"""
    event_id: str
    event_type: str
    event_data: dict

class EventUpdateSchema(BaseModel):
    """Schema to update event"""
    event_type: str = None
    event_data: dict = None

# -------------------------------
# POST: Create new event
# -------------------------------
@router.post("/create_event", tags=["events"])
def handle_event(data: Union[EventSchema, List[EventSchema]]) -> Response:
    """Create a new event"""
    print("Received event:", data)
    EVENT_STORE.append(data.dict())
    return Response(
        content=json.dumps({"message": "Data received!"}),
        status_code=HTTPStatus.ACCEPTED,
    )

# -------------------------------
# GET: List all events
# -------------------------------
@router.get("/get_all_events", tags=["events"])
def list_events():
    """Return all events"""
    return {"events": EVENT_STORE}

# -------------------------------
# GET: Get a single event by ID
# -------------------------------
@router.get("/{event_id}", tags=["events"])
def get_event(event_id: str = Path(..., description="ID of the event")):
    """Get a specific event by ID"""
    for event in EVENT_STORE:
        if event["event_id"] == event_id:
            return event
    return Response(
        content=json.dumps({"error": "Event not found"}),
        status_code=HTTPStatus.NOT_FOUND
    )

# -------------------------------
# PUT: Update an event
# -------------------------------
@router.put("/{event_id}", tags=["events"])
def update_event(event_id: str, data: EventUpdateSchema):
    """Update event type or data"""
    for event in EVENT_STORE:
        if event["event_id"] == event_id:
            if data.event_type is not None:
                event["event_type"] = data.event_type
            if data.event_data is not None:
                event["event_data"] = data.event_data
            return {"message": "Event updated", "event": event}
    return Response(
        content=json.dumps({"error": "Event not found"}),
        status_code=HTTPStatus.NOT_FOUND
    )

# -------------------------------
# DELETE: Remove an event
# -------------------------------
@router.delete("/{event_id}", tags=["events"])
def delete_event(event_id: str):
    """Delete an event by ID"""
    for i, event in enumerate(EVENT_STORE):
        if event["event_id"] == event_id:
            EVENT_STORE.pop(i)
            return {"message": f"Event {event_id} deleted"}
    return Response(
        content=json.dumps({"error": "Event not found"}),
        status_code=HTTPStatus.NOT_FOUND
    )

# -------------------------------
# GET: Search events by type using query param
# -------------------------------
@router.get("/search/", tags=["events"])
def search_events(event_type: str = Query(..., description="Type of event to search")):
    """Search events by event_type"""
    result = [e for e in EVENT_STORE if e["event_type"] == event_type]
    return {"results": result}
