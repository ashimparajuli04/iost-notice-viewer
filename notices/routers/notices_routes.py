from typing import Annotated
from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, func, select

from database import get_session
from notices.models.notice import Notice
from notices.services.notice_service import seed_notices


router = APIRouter(
    prefix="/notices",
    tags=["notices"],
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.post(
    "/seed"
)
def scrape_notices_to_db(
    session: Session = Depends(get_session)
):
    try:
        count = seed_notices(session)  # return count from seed_notices
        if count == 0:
            return JSONResponse(
                status_code=200,
                content={"message": "No new notices to seed"}
            )
        return JSONResponse(
            status_code=201,
            content={"message": f"Successfully seeded {count} notices"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
def get_notices(
    session: Session = Depends(get_session),
    page: int = 1,
    page_size: int = 10,
):
    offset = (page - 1) * page_size
    
    total = session.exec(select(func.count(Notice.id))).one()
    notices = session.exec(
        select(Notice)
        .order_by(Notice.notice_number.desc())
        .offset(offset)
        .limit(page_size)
    ).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": -(-total // page_size),  # ceiling division
        "data": notices,
    }