from fastapi import APIRouter, Depends, HTTPException

from api.services.patient_service import PatientService

from sqlalchemy.orm import Session

from api.database.session import get_db

from api.schemas.patient import PatientTestSummary

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.get("")
def all_patients():
    return PatientService.all()

@router.get("/{sample_id}")
def by_sample(sample_id: str):
    return PatientService.sample(sample_id)

@router.get("/activity/{activity}")
def by_activity(activity: str):
    return PatientService.activity(activity)

@router.get("/assay/{assay}")
def by_assay(assay: str):
    return PatientService.assay(assay)







@router.get(
    "/tests/{sample_id}",
    response_model=PatientTestSummary
)
def tests_per_patient(
    sample_id: str,
    db: Session = Depends(get_db)
):

    result = PatientService.get_tests_per_patient(
        db,
        sample_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Sample not found"
        )

    return result