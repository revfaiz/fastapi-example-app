from fastapi import APIRouter, Path, Query
from pydantic import BaseModel
from typing import List, Union
from http import HTTPStatus
from starlette.responses import Response
import json

router = APIRouter()  # Events router

EVENT_STORE = []

class EventSchema(BaseModel):
    event_id: str
    event_type: str
    event_data: dict

class EventUpdateSchema(BaseModel):
    event_type: str = None
    event_data: dict = None

@router.post("/create_event")
def create_event(data: Union[EventSchema, List[EventSchema]]) -> Response:
    if isinstance(data, list):
        for d in data:
            EVENT_STORE.append(d.dict())
    else:
        EVENT_STORE.append(data.dict())
    return Response(json.dumps({"message": "Event(s) created!"}), status_code=HTTPStatus.CREATED)

@router.get("/get_all_events")
def get_all_events():
    return {"events": EVENT_STORE}

@router.get("/{event_id}")
def get_event(event_id: str = Path(...)):
    for event in EVENT_STORE:
        if event["event_id"] == event_id:
            return event
    return Response(json.dumps({"error": "Event not found"}), status_code=HTTPStatus.NOT_FOUND)

@router.put("/{event_id}")
def update_event(event_id: str, data: EventUpdateSchema):
    for event in EVENT_STORE:
        if event["event_id"] == event_id:
            if data.event_type:
                event["event_type"] = data.event_type
            if data.event_data:
                event["event_data"] = data.event_data
            return {"message": "Event updated", "event": event}
    return Response(json.dumps({"error": "Event not found"}), status_code=HTTPStatus.NOT_FOUND)

@router.delete("/{event_id}")
def delete_event(event_id: str):
    for i, event in enumerate(EVENT_STORE):
        if event["event_id"] == event_id:
            EVENT_STORE.pop(i)
            return {"message": f"Event {event_id} deleted"}
    return Response(json.dumps({"error": "Event not found"}), status_code=HTTPStatus.NOT_FOUND)

@router.get("/search")
def search_events(event_type: str = Query(...)):
    results = [e for e in EVENT_STORE if e["event_type"] == event_type]
    return {"results": results}
