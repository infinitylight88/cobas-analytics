from fastapi import APIRouter

from api.services.calibration_service import CalibrationService

router = APIRouter(
    prefix="/calibrations",
    tags=["Calibrations"]
)

@router.get("")
def all():
    return CalibrationService.all()



@router.get("/date/{target_date}")
def calibrations_by_date(target_date: str):
    return CalibrationService.by_date(target_date)


@router.get("/analyte/{analyte}")
def calibration_history(analyte: str):
    return CalibrationService.by_analyte(analyte)


@router.get("/summary")
def calibration_summary():
    return CalibrationService.summary()