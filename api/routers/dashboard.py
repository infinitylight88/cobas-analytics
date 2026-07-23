from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from api.database.session import get_db
from api.services.dashboard_service import DashboardService
from api.schemas.dashboard import DailyWorkload

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def summary():

    return DashboardService.summary()


@router.get("/activity")
def activity():

    return DashboardService.activity()


@router.get(
    "/daily-workload",
    response_model=DailyWorkload
)
def daily_workload(
    target_date: date,
    db: Session = Depends(get_db)
):

    return DashboardService.daily_workload(
        db,
        target_date
    )