from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.hba1c_service import HbA1cService

router = APIRouter(prefix="/hba1c", tags=["HbA1c"])
service = HbA1cService()


@router.get("/patients")
def hba1c_patients(db: Session = Depends(get_db)):
    return service.get_patients(db)


@router.get("/controls")
def hba1c_controls(db: Session = Depends(get_db)):
    return service.get_controls(db)


@router.get("/control-history")
def hba1c_control_history(db: Session = Depends(get_db)):
    return service.get_control_history(db)


@router.get("/qc-compliance")
def hba1c_qc_compliance(db: Session = Depends(get_db)):
    return service.get_qc_compliance(db)


@router.get("/statistics")
def hba1c_statistics(db: Session = Depends(get_db)):
    return service.get_statistics(db)


@router.get("/export")
def hba1c_export(db: Session = Depends(get_db)):
    buf = service.export_excel(db)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=hba1c_export.xlsx"},
    )


@router.get("/date/{target_date}")
def hba1c_by_date(target_date: str, db: Session = Depends(get_db)):
    return service.get_by_date(db, target_date)


@router.get("/patient/{patient_identifier}")
def hba1c_patient(patient_identifier: str, db: Session = Depends(get_db)):
    return service.get_patient_results(db, patient_identifier)
