from sqlmodel import Column, DateTime, SQLModel, Field
from datetime import datetime, timezone

class Notice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    notice_number: int = Field(unique=True, index=True)
    link: str
    date: datetime = Field(
            sa_column=Column(DateTime(timezone=True), nullable=False),
            default_factory=lambda: datetime.now(timezone.utc),
        )