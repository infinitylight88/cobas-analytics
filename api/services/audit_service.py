from datetime import date

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from api.database.models import ArchiveFile, Calibration, PatientResult, QCResult


class AuditService:

    def qc_before_patients(self, db: Session):
        """
        For each day that patient results exist, check if QC was run
        before the first patient result of that day.
        """
        patient_first = (
            db.query(
                func.date(PatientResult.run_datetime).label("day"),
                func.min(PatientResult.run_datetime).label("first_patient"),
            )
            .group_by(func.date(PatientResult.run_datetime))
            .all()
        )
        result = []
        for row in sorted(patient_first, key=lambda x: x.day):
            d = row.day
            first_qc = (
                db.query(func.min(QCResult.run_datetime))
                .filter(func.date(QCResult.run_datetime) == d)
                .scalar()
            )
            qc_before = first_qc is not None and first_qc <= row.first_patient
            result.append({
                "date": str(d),
                "first_patient_result": str(row.first_patient),
                "first_qc_run": str(first_qc) if first_qc else None,
                "qc_before_patients": qc_before,
                "status": "PASS" if qc_before else "FAIL",
            })
        return result

    def qc_for_day(self, db: Session, target_date: str):
        d = date.fromisoformat(target_date)
        qc_rows = (
            db.query(QCResult)
            .filter(func.date(QCResult.run_datetime) == d)
            .order_by(QCResult.run_datetime)
            .all()
        )
        return {
            "date": target_date,
            "total_runs": len(qc_rows),
            "analytes_tested": sorted({r.analyte_code for r in qc_rows}),
            "controls_used": sorted({r.control_name for r in qc_rows if r.control_name}),
            "results": [
                {
                    "qc_id": r.qc_id,
                    "run_datetime": str(r.run_datetime),
                    "analyte_code": r.analyte_code,
                    "control_name": r.control_name,
                    "control_lot": r.control_lot,
                    "measured_value": float(r.measured_value) if r.measured_value else None,
                    "assigned_value": float(r.assigned_value) if r.assigned_value else None,
                    "units": r.units,
                }
                for r in qc_rows
            ],
        }

    def calibration_history(self, db: Session):
        rows = (
            db.query(Calibration)
            .order_by(Calibration.analyte_code, Calibration.run_datetime.asc())
            .all()
        )
        return [
            {
                "calibration_id": r.calibration_id,
                "analyte_code": r.analyte_code,
                "run_datetime": str(r.run_datetime),
                "calibration_type": r.calibration_type,
                "reagent_lot": r.reagent_lot,
                "slope": float(r.slope) if r.slope else None,
                "offset": float(r.offset) if r.offset else None,
                "factor": float(r.factor) if r.factor else None,
            }
            for r in rows
        ]

    def reagent_history(self, db: Session):
        cal_rows = (
            db.query(
                Calibration.analyte_code,
                Calibration.reagent_lot,
                func.min(Calibration.run_datetime).label("first_use"),
                func.max(Calibration.run_datetime).label("last_use"),
                func.count(Calibration.calibration_id).label("calibrations"),
            )
            .filter(Calibration.reagent_lot.isnot(None))
            .group_by(Calibration.analyte_code, Calibration.reagent_lot)
            .order_by(Calibration.analyte_code, func.min(Calibration.run_datetime))
            .all()
        )
        return [
            {
                "analyte_code": r.analyte_code,
                "reagent_lot": r.reagent_lot,
                "first_use": str(r.first_use),
                "last_use": str(r.last_use),
                "calibrations": r.calibrations,
            }
            for r in cal_rows
        ]

    def instrument_events(self, db: Session):
        rows = db.execute(
            text(
                """
                SELECT 'maintenance' AS event_type, run_datetime, maintenance_type AS description,
                       maintenance_code AS code
                FROM maintenance
                UNION ALL
                SELECT 'host_event', run_datetime, event_text, event_code
                FROM host_events
                ORDER BY run_datetime DESC
                """
            )
        ).fetchall()
        return [
            {
                "event_type": r[0],
                "run_datetime": str(r[1]),
                "description": r[2],
                "code": r[3],
            }
            for r in rows
        ]

    def operator_activity(self, db: Session):
        rows = (
            db.query(ArchiveFile)
            .order_by(ArchiveFile.archive_start.desc())
            .all()
        )
        return [
            {
                "archive_id": r.archive_id,
                "filename": r.filename,
                "operator_name": r.operator_name,
                "archive_start": str(r.archive_start) if r.archive_start else None,
                "archive_end": str(r.archive_end) if r.archive_end else None,
                "imported_at": str(r.imported_at) if r.imported_at else None,
            }
            for r in rows
        ]

    def sample_trace(self, db: Session, sample_id: str):
        rows = (
            db.query(PatientResult)
            .filter(PatientResult.sample_id == sample_id)
            .order_by(PatientResult.run_datetime)
            .all()
        )
        if not rows:
            return {"sample_id": sample_id, "found": False}
        first = rows[0]
        return {
            "sample_id": sample_id,
            "found": True,
            "patient_identifier": first.patient_identifier,
            "patient_initials": first.patient_initials,
            "patient_program": first.patient_program,
            "sample_type": first.sample_type,
            "total_tests": len(rows),
            "results": [
                {
                    "result_id": r.result_id,
                    "run_datetime": str(r.run_datetime),
                    "analyte_code": r.analyte_code,
                    "analyte_name": r.analyte_name,
                    "result_value": float(r.result_value) if r.result_value is not None else None,
                    "units": r.units,
                    "reference_flag": r.reference_flag,
                    "status": r.status,
                    "instrument_position": r.instrument_position,
                    "raw_id": r.raw_id,
                }
                for r in rows
            ],
        }

    def archive_audit(self, db: Session, archive_id: int):
        archive = db.query(ArchiveFile).filter(ArchiveFile.archive_id == archive_id).first()
        if not archive:
            return {"archive_id": archive_id, "found": False}
        patient_count = db.query(func.count(PatientResult.result_id)).filter(PatientResult.archive_id == archive_id).scalar()
        qc_count = db.query(func.count(QCResult.qc_id)).filter(QCResult.archive_id == archive_id).scalar()
        cal_count = db.query(func.count(Calibration.calibration_id)).filter(Calibration.archive_id == archive_id).scalar()
        log = db.execute(
            text("SELECT lines_read, parsed_ok, errors, parser_version, logged_at FROM parser_log WHERE archive_id = :aid"),
            {"aid": archive_id},
        ).fetchone()
        return {
            "archive_id": archive_id,
            "filename": archive.filename,
            "operator_name": archive.operator_name,
            "archive_start": str(archive.archive_start) if archive.archive_start else None,
            "archive_end": str(archive.archive_end) if archive.archive_end else None,
            "imported_at": str(archive.imported_at) if archive.imported_at else None,
            "patient_results": patient_count,
            "qc_results": qc_count,
            "calibrations": cal_count,
            "parser_log": {
                "lines_read": log[0], "parsed_ok": log[1], "errors": log[2],
                "parser_version": log[3], "logged_at": str(log[4]),
            } if log else None,
        }

    def get_report(self, db: Session):
        days = self.qc_before_patients(db)
        passed = sum(1 for d in days if d["status"] == "PASS")
        failed = sum(1 for d in days if d["status"] == "FAIL")
        return {
            "summary": {
                "total_days_analyzed": len(days),
                "qc_before_patients_pass": passed,
                "qc_before_patients_fail": failed,
                "compliance_pct": round(passed * 100 / len(days), 2) if days else 100,
            },
            "daily_qc_compliance": days,
        }
