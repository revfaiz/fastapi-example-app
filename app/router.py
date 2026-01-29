from fastapi import APIRouter

from endpoints import events,users


router = APIRouter()

router.include_router(events.router, prefix="/events", tags=["events"])
router.include_router(users.router, prefix="/users", tags=["users"])


