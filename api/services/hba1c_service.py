import io
import statistics
from datetime import date

import openpyxl
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database.models import PatientResult, QCResult

HBA1C_GROUP = "HBA1C"


class HbA1cService:

    def get_patients(self, db: Session):
        rows = (
            db.query(
                PatientResult.patient_identifier,
                PatientResult.patient_initials,
                PatientResult.patient_program,
                func.count(PatientResult.result_id).label("tests"),
                func.min(PatientResult.run_datetime).label("first_run"),
                func.max(PatientResult.run_datetime).label("last_run"),
            )
            .filter(PatientResult.assay_group == HBA1C_GROUP)
            .group_by(
                PatientResult.patient_identifier,
                PatientResult.patient_initials,
                PatientResult.patient_program,
            )
            .order_by(PatientResult.patient_identifier)
            .all()
        )
        return [
            {
                "patient_identifier": r.patient_identifier,
                "patient_initials": r.patient_initials,
                "patient_program": r.patient_program,
                "tests": r.tests,
                "first_run": str(r.first_run),
                "last_run": str(r.last_run),
            }
            for r in rows
        ]

    def get_by_date(self, db: Session, target_date: str):
        d = date.fromisoformat(target_date)
        return (
            db.query(PatientResult)
            .filter(
                PatientResult.assay_group == HBA1C_GROUP,
                func.date(PatientResult.run_datetime) == d,
            )
            .order_by(PatientResult.run_datetime)
            .all()
        )

    def get_patient_results(self, db: Session, patient_identifier: str):
        return (
            db.query(PatientResult)
            .filter(
                PatientResult.assay_group == HBA1C_GROUP,
                PatientResult.patient_identifier == patient_identifier,
            )
            .order_by(PatientResult.run_datetime.asc())
            .all()
        )

    def get_controls(self, db: Session):
        rows = (
            db.query(
                QCResult.control_name,
                QCResult.control_lot,
                QCResult.analyte_code,
                func.count(QCResult.qc_id).label("runs"),
            )
            .filter(QCResult.assay_group == HBA1C_GROUP)
            .group_by(QCResult.control_name, QCResult.control_lot, QCResult.analyte_code)
            .order_by(QCResult.control_name)
            .all()
        )
        return [
            {
                "control_name": r.control_name,
                "control_lot": r.control_lot,
                "analyte_code": r.analyte_code,
                "runs": r.runs,
            }
            for r in rows
        ]

    def get_control_history(self, db: Session):
        return (
            db.query(QCResult)
            .filter(QCResult.assay_group == HBA1C_GROUP)
            .order_by(QCResult.run_datetime.asc())
            .all()
        )

    def get_qc_compliance(self, db: Session):
        dates = (
            db.query(func.date(PatientResult.run_datetime).label("d"))
            .filter(PatientResult.assay_group == HBA1C_GROUP)
            .distinct()
            .all()
        )
        result = []
        for row in sorted(dates, key=lambda x: x.d):
            d = row.d
            patient_analytes = {
                r[0] for r in
                db.query(PatientResult.analyte_code)
                .filter(PatientResult.assay_group == HBA1C_GROUP, func.date(PatientResult.run_datetime) == d)
                .distinct().all()
            }
            qc_analytes = {
                r[0] for r in
                db.query(QCResult.analyte_code)
                .filter(QCResult.assay_group == HBA1C_GROUP, func.date(QCResult.run_datetime) == d)
                .distinct().all()
            }
            performed = len(patient_analytes & qc_analytes)
            required = len(patient_analytes)
            result.append({
                "date": str(d),
                "required": required,
                "performed": performed,
                "missing": required - performed,
                "compliance_pct": round(performed * 100 / required, 2) if required else 100,
            })
        return result

    def get_statistics(self, db: Session):
        rows = (
            db.query(PatientResult)
            .filter(PatientResult.assay_group == HBA1C_GROUP, PatientResult.result_value.isnot(None))
            .all()
        )
        if not rows:
            return {"message": "No HbA1c results found"}
        values = [float(r.result_value) for r in rows if r.result_value is not None]
        n = len(values)
        mean_v = sum(values) / n
        sd_v = statistics.stdev(values) if n > 1 else 0.0
        return {
            "total_results": n,
            "unique_patients": len({r.patient_identifier for r in rows}),
            "mean": round(mean_v, 2),
            "sd": round(sd_v, 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "units": rows[0].units if rows else None,
        }

    def export_excel(self, db: Session):
        rows = (
            db.query(PatientResult)
            .filter(PatientResult.assay_group == HBA1C_GROUP)
            .order_by(PatientResult.run_datetime.desc())
            .all()
        )
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "HbA1c Results"
        ws.append([
            "Result ID", "Run DateTime", "Patient ID", "Patient Initials",
            "Sample ID", "Analyte Code", "Result Value", "Units",
            "Reference Flag", "Status", "Program",
        ])
        for r in rows:
            ws.append([
                r.result_id, str(r.run_datetime), r.patient_identifier, r.patient_initials,
                r.sample_id, r.analyte_code,
                float(r.result_value) if r.result_value else None,
                r.units, r.reference_flag, r.status, r.patient_program,
            ])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf
