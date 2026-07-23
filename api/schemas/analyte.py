from datetime import date, datetime
from pydantic import BaseModel


class ArchiveResponse(BaseModel):

    archive_id: int
    filename: str
    archive_start: date | None
    archive_end: date | None
    operator_name: str | None
    archive_version: str | None
    imported_at: datetime | None


    class Config:
        from_attributes = True