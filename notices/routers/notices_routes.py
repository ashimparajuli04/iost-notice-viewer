from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from notices.models.notice import Notice
from notices.services.notice_service import create_notice


router = APIRouter(
    prefix="/notices",
    tags=["notices"],
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/",
    response_model=Notice,
)
def create_menu_category(
    data: Notice,
    session: Session = Depends(get_session)
):
    return create_notice(session, data)