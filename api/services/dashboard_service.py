from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database.models import ArchiveFile, Calibration, PatientResult, QCResult


class DashboardService:

    def summary(self, db: Session):
        return {
            "patients": db.query(PatientResult).count(),
            "qc": db.query(QCResult).count(),
            "calibrations": db.query(Calibration).count(),
            "archives": db.query(ArchiveFile).count(),
        }

    def activity(self, db: Session):
        rows = (
            db.query(
                func.date(PatientResult.run_datetime).label("date"),
                func.count(PatientResult.result_id).label("patient_results"),
            )
            .group_by(func.date(PatientResult.run_datetime))
            .order_by(func.date(PatientResult.run_datetime).desc())
            .limit(30)
            .all()
        )
        return [{"date": str(r.date), "patient_results": r.patient_results} for r in rows]

    def daily_workload(self, db: Session, target_date):
        result = (
            db.query(
                func.count(func.distinct(PatientResult.sample_id)).label("samples")
            )
            .filter(func.date(PatientResult.run_datetime) == target_date)
            .first()
        )
        return {"date": str(target_date), "unique_samples": result.samples or 0}

    def analytes_run_on_date(self, db: Session, target_date):
        return (
            db.query(PatientResult.analyte_code)
            .filter(func.date(PatientResult.run_datetime) == target_date)
            .distinct()
            .all()
        )

    def monthly_workload(self, db: Session):
        rows = (
            db.query(
                func.to_char(PatientResult.run_datetime, "YYYY-MM").label("month"),
                func.count(func.distinct(PatientResult.sample_id)).label("unique_samples"),
                func.count(func.distinct(PatientResult.patient_identifier)).label("unique_patients"),
                func.count(PatientResult.result_id).label("total_results"),
            )
            .group_by(func.to_char(PatientResult.run_datetime, "YYYY-MM"))
            .order_by(func.to_char(PatientResult.run_datetime, "YYYY-MM"))
            .all()
        )
        return [
            {
                "month": r.month,
                "unique_samples": r.unique_samples,
                "unique_patients": r.unique_patients,
                "total_results": r.total_results,
            }
            for r in rows
        ]

    def operator_summary(self, db: Session):
        rows = (
            db.query(
                ArchiveFile.operator_name,
                func.count(ArchiveFile.archive_id).label("archives"),
                func.min(ArchiveFile.archive_start).label("earliest"),
                func.max(ArchiveFile.archive_end).label("latest"),
            )
            .group_by(ArchiveFile.operator_name)
            .order_by(func.count(ArchiveFile.archive_id).desc())
            .all()
        )
        return [
            {
                "operator_name": r.operator_name,
                "archives": r.archives,
                "earliest_archive": str(r.earliest) if r.earliest else None,
                "latest_archive": str(r.latest) if r.latest else None,
            }
            for r in rows
        ]

    def reagent_usage(self, db: Session):
        cal_rows = (
            db.query(
                Calibration.reagent_lot,
                Calibration.analyte_code,
                func.count(Calibration.calibration_id).label("calibrations"),
                func.min(Calibration.run_datetime).label("first_use"),
                func.max(Calibration.run_datetime).label("last_use"),
            )
            .filter(Calibration.reagent_lot.isnot(None))
            .group_by(Calibration.reagent_lot, Calibration.analyte_code)
            .order_by(Calibration.analyte_code, Calibration.reagent_lot)
            .all()
        )
        qc_rows = (
            db.query(
                QCResult.reagent_lot,
                QCResult.analyte_code,
                func.count(QCResult.qc_id).label("qc_runs"),
            )
            .filter(QCResult.reagent_lot.isnot(None))
            .group_by(QCResult.reagent_lot, QCResult.analyte_code)
            .all()
        )
        qc_map = {(r.analyte_code, r.reagent_lot): r.qc_runs for r in qc_rows}
        return [
            {
                "analyte_code": r.analyte_code,
                "reagent_lot": r.reagent_lot,
                "calibrations": r.calibrations,
                "qc_runs": qc_map.get((r.analyte_code, r.reagent_lot), 0),
                "first_use": str(r.first_use),
                "last_use": str(r.last_use),
            }
            for r in cal_rows
        ]

    def instrument_utilization(self, db: Session):
        rows = (
            db.query(
                func.date(PatientResult.run_datetime).label("date"),
                func.count(func.distinct(PatientResult.sample_id)).label("samples"),
                func.count(PatientResult.result_id).label("tests"),
                func.count(func.distinct(PatientResult.analyte_code)).label("analytes"),
            )
            .group_by(func.date(PatientResult.run_datetime))
            .order_by(func.date(PatientResult.run_datetime))
            .all()
        )
        return [
            {
                "date": str(r.date),
                "unique_samples": r.samples,
                "total_tests": r.tests,
                "analytes_run": r.analytes,
            }
            for r in rows
        ]

    def turnaround_time(self, db: Session):
        return {
            "message": "Turnaround time requires request timestamps not present in the archive format.",
            "available": False,
        }

    def activity_summary(self, db: Session):
        patient_rows = (
            db.query(
                func.date(PatientResult.run_datetime).label("date"),
                func.count(PatientResult.result_id).label("patient_results"),
                func.count(func.distinct(PatientResult.sample_id)).label("unique_samples"),
            )
            .group_by(func.date(PatientResult.run_datetime))
            .all()
        )
        qc_rows = (
            db.query(
                func.date(QCResult.run_datetime).label("date"),
                func.count(QCResult.qc_id).label("qc_runs"),
            )
            .group_by(func.date(QCResult.run_datetime))
            .all()
        )
        cal_rows = (
            db.query(
                func.date(Calibration.run_datetime).label("date"),
                func.count(Calibration.calibration_id).label("calibrations"),
            )
            .group_by(func.date(Calibration.run_datetime))
            .all()
        )
        qc_map = {str(r.date): r.qc_runs for r in qc_rows}
        cal_map = {str(r.date): r.calibrations for r in cal_rows}
        result = []
        for r in sorted(patient_rows, key=lambda x: x.date):
            d = str(r.date)
            result.append({
                "date": d,
                "patient_results": r.patient_results,
                "unique_samples": r.unique_samples,
                "qc_runs": qc_map.get(d, 0),
                "calibrations": cal_map.get(d, 0),
            })
        return result
