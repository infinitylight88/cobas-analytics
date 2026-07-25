from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.analyte_service import AnalyteService

router = APIRouter(prefix="/analytes", tags=["Analytes"])
service = AnalyteService()


@router.get("")
def all_analytes(db: Session = Depends(get_db)):
    return service.get_all(db)


@router.get("/summary")
def analyte_summary(db: Session = Depends(get_db)):
    return service.get_summary(db)


@router.get("/chemistry")
def chemistry_analytes(db: Session = Depends(get_db)):
    return service.get_chemistry(db)


@router.get("/hba1c")
def hba1c_analytes(db: Session = Depends(get_db)):
    return service.get_hba1c(db)


@router.get("/ise")
def ise_analytes(db: Session = Depends(get_db)):
    return service.get_ise(db)


@router.get("/{analyte}")
def analyte_results(analyte: str, db: Session = Depends(get_db)):
    return service.get_by_code(db, analyte)
