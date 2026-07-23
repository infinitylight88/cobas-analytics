from fastapi import APIRouter

from api.services.archive_service import ArchiveService

router = APIRouter(
    prefix="/archives",
    tags=["Archives"]
)

@router.get("")
def all():
    return ArchiveService.all()