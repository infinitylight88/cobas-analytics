from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.system_service import SystemService

router = APIRouter(
    prefix="/system",
    tags=["System"]
)


@router.get("/status")
def system_status(db: Session = Depends(get_db)):

    service = SystemService(db)

    return service.status()