from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.calibration_service import CalibrationService

router = APIRouter(prefix="/calibrations", tags=["Calibrations"])
service = CalibrationService()


@router.get("")
def all_calibrations(db: Session = Depends(get_db)):
    return service.all(db)


@router.get("/date/{target_date}")
def calibrations_by_date(target_date: str, db: Session = Depends(get_db)):
    return service.by_date(db, target_date)


@router.get("/summary")
def calibration_summary(db: Session = Depends(get_db)):
    return service.get_summary(db)


@router.get("/expired")
def calibrations_expired(days: int = 30, db: Session = Depends(get_db)):
    return service.get_expired(db, days)


@router.get("/export")
def calibrations_export(db: Session = Depends(get_db)):
    buf = service.export_excel(db)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=calibrations_export.xlsx"},
    )


@router.get("/reagent/{lot}")
def calibrations_by_reagent(lot: str, db: Session = Depends(get_db)):
    return service.by_reagent(db, lot)


@router.get("/analyte/{analyte}")
def calibrations_by_analyte(analyte: str, db: Session = Depends(get_db)):
    return service.by_analyte(db, analyte)


@router.get("/history/{analyte}")
def calibration_history(analyte: str, db: Session = Depends(get_db)):
    return service.history(db, analyte)
