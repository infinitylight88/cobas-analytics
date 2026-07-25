from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.qc_service import QCService

router = APIRouter(prefix="/qc", tags=["Quality Control"])
service = QCService()


@router.get("/date/{target_date}")
def qc_by_date(target_date: str, db: Session = Depends(get_db)):
    return service.get_by_date(db, target_date)


@router.get("/analyte/{analyte}")
def qc_by_analyte(analyte: str, db: Session = Depends(get_db)):
    return service.get_by_analyte(db, analyte)


@router.get("/summary")
def qc_summary(db: Session = Depends(get_db)):
    return service.get_summary(db)


@router.get("/compliance")
def qc_compliance(target_date: str, db: Session = Depends(get_db)):
    return service.get_compliance(db, target_date)


@router.get("/missing")
def qc_missing(target_date: str, db: Session = Depends(get_db)):
    return service.get_missing(db, target_date)


@router.get("/statistics")
def qc_statistics(db: Session = Depends(get_db)):
    return service.get_statistics(db)


@router.get("/outliers")
def qc_outliers(db: Session = Depends(get_db)):
    return service.get_outliers(db)


@router.get("/export")
def qc_export(db: Session = Depends(get_db)):
    buf = service.export_excel(db)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=qc_export.xlsx"},
    )


@router.get("/history/{analyte}")
def qc_history(analyte: str, db: Session = Depends(get_db)):
    return service.get_history(db, analyte)


@router.get("/control/{control_name}")
def qc_by_control(control_name: str, db: Session = Depends(get_db)):
    return service.get_by_control(db, control_name)


@router.get("/control-lot/{lot}")
def qc_by_lot(lot: str, db: Session = Depends(get_db)):
    return service.get_by_lot(db, lot)


@router.get("/levy-jennings/{analyte}")
def levy_jennings(analyte: str, db: Session = Depends(get_db)):
    return service.get_levy_jennings(db, analyte)


@router.get("/westgard/{analyte}")
def westgard(analyte: str, db: Session = Depends(get_db)):
    return service.get_westgard(db, analyte)
