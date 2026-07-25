from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])
service = ReportService()


@router.get("/daily")
def daily_report(target_date: str, db: Session = Depends(get_db)):
    return service.daily(db, target_date)


@router.get("/monthly")
def monthly_report(year: int, month: int, db: Session = Depends(get_db)):
    return service.monthly(db, year, month)


@router.get("/qc")
def qc_report(db: Session = Depends(get_db)):
    return service.qc_report(db)


@router.get("/calibration")
def calibration_report(db: Session = Depends(get_db)):
    return service.calibration_report(db)


@router.get("/actg")
def actg_report(db: Session = Depends(get_db)):
    return service.actg_report(db)


@router.get("/workload")
def workload_report(db: Session = Depends(get_db)):
    return service.workload_report(db)


@router.get("/export/excel")
def export_excel(db: Session = Depends(get_db)):
    buf = service.export_excel(db)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=cobas_report.xlsx"},
    )


@router.get("/export/pdf")
def export_pdf(db: Session = Depends(get_db)):
    # PDF generation requires a dedicated library (e.g. reportlab or weasyprint).
    # Returning a JSON summary until a PDF library is added.
    return {
        "message": "PDF export not yet available. Use /reports/export/excel for a full data export.",
        "available_exports": ["/reports/export/excel"],
    }
