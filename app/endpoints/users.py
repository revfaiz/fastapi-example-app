from fastapi import APIRouter, Path, Query
from pydantic import BaseModel
from typing import List, Union
from http import HTTPStatus
from starlette.responses import Response
import json

router = APIRouter()  # Users router

USER_STORE = []

class UserSchema(BaseModel):
    user_id: str
    name: str
    email: str

class UserUpdateSchema(BaseModel):
    name: str = None
    email: str = None

@router.post("/create_user")
def create_user(data: Union[UserSchema, List[UserSchema]]) -> Response:
    if isinstance(data, list):
        for user in data:
            USER_STORE.append(user.dict())
    else:
        USER_STORE.append(data.dict())
    return Response(json.dumps({"message": "User(s) created!"}), status_code=HTTPStatus.CREATED)

@router.get("/get_all_users")
def get_all_users():
    return {"users": USER_STORE}

@router.get("/{user_id}")
def get_user(user_id: str = Path(...)):
    for user in USER_STORE:
        if user["user_id"] == user_id:
            return user
    return Response(json.dumps({"error": "User not found"}), status_code=HTTPStatus.NOT_FOUND)

@router.put("/{user_id}")
def update_user(user_id: str, data: UserUpdateSchema):
    for user in USER_STORE:
        if user["user_id"] == user_id:
            if data.name:
                user["name"] = data.name
            if data.email:
                user["email"] = data.email
            return {"message": "User updated", "user": user}
    return Response(json.dumps({"error": "User not found"}), status_code=HTTPStatus.NOT_FOUND)

@router.delete("/{user_id}")
def delete_user(user_id: str):
    for i, user in enumerate(USER_STORE):
        if user["user_id"] == user_id:
            USER_STORE.pop(i)
            return {"message": f"User {user_id} deleted"}
    return Response(json.dumps({"error": "User not found"}), status_code=HTTPStatus.NOT_FOUND)

@router.get("/search")
def search_users(name: str = Query(None), email: str = Query(None)):
    results = [
        u for u in USER_STORE
        if (name and name.lower() in u["name"].lower()) or
           (email and email.lower() in u["email"].lower())
    ]
    return {"results": results}
