from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.schemas.dashboard import DailyWorkload
from api.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
service = DashboardService()


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return service.summary(db)


@router.get("/activity")
def activity(db: Session = Depends(get_db)):
    return service.activity(db)


@router.get("/daily-workload", response_model=DailyWorkload)
def daily_workload(target_date: date, db: Session = Depends(get_db)):
    return service.daily_workload(db, target_date)


@router.get("/monthly-workload")
def monthly_workload(db: Session = Depends(get_db)):
    return service.monthly_workload(db)


@router.get("/operator-summary")
def operator_summary(db: Session = Depends(get_db)):
    return service.operator_summary(db)


@router.get("/reagent-usage")
def reagent_usage(db: Session = Depends(get_db)):
    return service.reagent_usage(db)


@router.get("/instrument-utilization")
def instrument_utilization(db: Session = Depends(get_db)):
    return service.instrument_utilization(db)


@router.get("/turnaround-time")
def turnaround_time(db: Session = Depends(get_db)):
    return service.turnaround_time(db)


@router.get("/activity-summary")
def activity_summary(db: Session = Depends(get_db)):
    return service.activity_summary(db)


@router.get("/analytes-per-day")
def analytes_per_day(target_date: date, db: Session = Depends(get_db)):
    rows = service.analytes_run_on_date(db, target_date)
    return {"date": str(target_date), "analytes": [r[0] for r in rows]}


@router.get("/department-summary")
def department_summary(db: Session = Depends(get_db)):
    return service.summary(db)


@router.get("/tests-per-patient")
def tests_per_patient(db: Session = Depends(get_db)):
    return service.activity(db)
