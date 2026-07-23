from fastapi import APIRouter, Depends
from datetime import date

from api.database.session import get_db
from api.services.actg_service import ACTGService


router = APIRouter(
    prefix="/actg",
    tags=["ACTG"]
)



@router.get("/patients")
def actg_patients(
    db=Depends(get_db)
):

    return ACTGService.patients(db)



@router.get("/{patient_id}")
def actg_patient_history(
    patient_id:str,
    db=Depends(get_db)
):

    return ACTGService.patient_results(
        db,
        patient_id
    )



@router.get("/workload/{target_date}")
def actg_workload(
    target_date:date,
    db=Depends(get_db)
):

    return ACTGService.workload(
        db,
        target_date
    )