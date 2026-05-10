from sqlmodel import SQLModel
from datetime import datetime

class NoticeCreate(SQLModel):
    title: str
    notice_number: int
    link: str
    date: datetime