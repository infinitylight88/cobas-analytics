from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.qc_service import QCService

router = APIRouter(
    prefix="/qc",
    tags=["Quality Control"]
)

service = QCService()


@router.get("/date/{target_date}")
def qc_by_date(target_date: str,
               db: Session = Depends(get_db)):
    return service.get_by_date(db, target_date)


@router.get("/analyte/{analyte}")
def qc_by_analyte(analyte: str,
                  db: Session = Depends(get_db)):
    return service.get_by_analyte(db, analyte)


@router.get("/summary")
def qc_summary(db: Session = Depends(get_db)):
    return service.get_summary(db)


@router.get("/compliance")
def qc_compliance(target_date: str,
                  db: Session = Depends(get_db)):
    return service.get_compliance(db, target_date)


@router.get("/missing")
def qc_missing(target_date: str,
               db: Session = Depends(get_db)):
    return service.get_missing(db, target_date)