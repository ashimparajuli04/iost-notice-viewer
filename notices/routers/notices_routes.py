from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from notices.models.notice import Notice
from notices.services.notice_service import seed_notices


router = APIRouter(
    prefix="/notices",
    tags=["notices"],
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/seed",
    response_model=Notice,
)
def create_initial_notice(
    session: Session = Depends(get_session)
):
    try:
        seed_notices(session)
        return {"message": "Notices seeded successfully"}
    except Exception as e:
        return {"Failed to seed notices": str(e)}