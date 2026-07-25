from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.actg_service import ACTGService

router = APIRouter(prefix="/actg", tags=["ACTG"])
service = ACTGService()


@router.get("")
def actg_all(db: Session = Depends(get_db)):
    return service.all_results(db)


@router.get("/patients")
def actg_patients(db: Session = Depends(get_db)):
    return service.patients(db)


@router.get("/workload")
def actg_workload(target_date: str, db: Session = Depends(get_db)):
    return service.workload(db, target_date)


@router.get("/monthly")
def actg_monthly(db: Session = Depends(get_db)):
    return service.monthly(db)


@router.get("/statistics")
def actg_statistics(db: Session = Depends(get_db)):
    return service.statistics(db)


@router.get("/export")
def actg_export(db: Session = Depends(get_db)):
    buf = service.export_excel(db)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=actg_export.xlsx"},
    )


@router.get("/date/{target_date}")
def actg_by_date(target_date: str, db: Session = Depends(get_db)):
    return service.by_date(db, target_date)


@router.get("/{patient_identifier}")
def actg_patient(patient_identifier: str, db: Session = Depends(get_db)):
    return service.patient_results(db, patient_identifier)
