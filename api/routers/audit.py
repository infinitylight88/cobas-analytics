from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["Audit"])
service = AuditService()


@router.get("/qc-before-patients")
def qc_before_patients(db: Session = Depends(get_db)):
    return service.qc_before_patients(db)


@router.get("/calibration-history")
def calibration_history(db: Session = Depends(get_db)):
    return service.calibration_history(db)


@router.get("/reagent-history")
def reagent_history(db: Session = Depends(get_db)):
    return service.reagent_history(db)


@router.get("/instrument-events")
def instrument_events(db: Session = Depends(get_db)):
    return service.instrument_events(db)


@router.get("/operator-activity")
def operator_activity(db: Session = Depends(get_db)):
    return service.operator_activity(db)


@router.get("/report")
def audit_report(db: Session = Depends(get_db)):
    return service.get_report(db)


@router.get("/qc-for-day/{target_date}")
def qc_for_day(target_date: str, db: Session = Depends(get_db)):
    return service.qc_for_day(db, target_date)


@router.get("/sample-trace/{sample_id}")
def sample_trace(sample_id: str, db: Session = Depends(get_db)):
    return service.sample_trace(db, sample_id)


@router.get("/archive/{archive_id}")
def archive_audit(archive_id: int, db: Session = Depends(get_db)):
    return service.archive_audit(db, archive_id)
