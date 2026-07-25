from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.schemas.patient import PatientTestSummary
from api.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])
service = PatientService()


@router.get("")
def all_patients(db: Session = Depends(get_db)):
    return service.all(db)


@router.get("/search")
def search_patients(q: str, db: Session = Depends(get_db)):
    return service.search(db, q)


@router.get("/day/{target_date}")
def patients_by_day(target_date: str, db: Session = Depends(get_db)):
    return service.by_day(db, target_date)


@router.get("/history/{patient_identifier}")
def patient_history(patient_identifier: str, db: Session = Depends(get_db)):
    result = service.get_history(db, patient_identifier)
    if result is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return result


@router.get("/analytes/{patient_identifier}")
def patient_analytes(patient_identifier: str, db: Session = Depends(get_db)):
    return service.get_analytes(db, patient_identifier)


@router.get("/tests/{sample_id}", response_model=PatientTestSummary)
def tests_per_patient(sample_id: str, db: Session = Depends(get_db)):
    result = service.get_tests_per_patient(db, sample_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return result


@router.get("/{patient_identifier}")
def patient_by_identifier(patient_identifier: str, db: Session = Depends(get_db)):
    return service.by_identifier(db, patient_identifier)
