from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.session import get_db

from api.services.archive_service import ArchiveService

from api.schemas.archive import ArchiveResponse


router = APIRouter(
    prefix="/archives",
    tags=["Archives"]
)



@router.get(
    "",
    response_model=list[ArchiveResponse]
)
def get_archives(
    db: Session = Depends(get_db)
):

    service = ArchiveService(db)

    return service.get_all()



@router.get(
    "/{archive_id}",
    response_model=ArchiveResponse
)
def get_archive(
    archive_id:int,
    db:Session=Depends(get_db)
):

    service = ArchiveService(db)

    archive = service.get_by_id(
        archive_id
    )


    if not archive:

        raise HTTPException(
            status_code=404,
            detail="Archive not found"
        )


    return archive