import io
from datetime import date

import openpyxl
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database.models import Patient, PatientResult

ACTG_PROGRAM = "ACTG"


class ACTGService:

    @staticmethod
    def patients(db: Session):
        return (
            db.query(Patient)
            .filter(Patient.patient_program == ACTG_PROGRAM)
            .all()
        )

    @staticmethod
    def all_results(db: Session):
        return (
            db.query(PatientResult)
            .filter(PatientResult.patient_program == ACTG_PROGRAM)
            .order_by(PatientResult.run_datetime.desc())
            .all()
        )

    @staticmethod
    def patient_results(db: Session, patient_id: str):
        return (
            db.query(PatientResult)
            .filter(PatientResult.patient_identifier == patient_id)
            .order_by(PatientResult.run_datetime.desc())
            .all()
        )

    @staticmethod
    def by_date(db: Session, target_date: str):
        d = date.fromisoformat(target_date)
        return (
            db.query(PatientResult)
            .filter(
                PatientResult.patient_program == ACTG_PROGRAM,
                func.date(PatientResult.run_datetime) == d,
            )
            .order_by(PatientResult.run_datetime)
            .all()
        )

    @staticmethod
    def workload(db: Session, target_date):
        if isinstance(target_date, str):
            target_date = date.fromisoformat(target_date)
        patients = (
            db.query(func.count(func.distinct(PatientResult.patient_identifier)))
            .filter(
                PatientResult.patient_program == ACTG_PROGRAM,
                func.date(PatientResult.run_datetime) == target_date,
            )
            .scalar()
        )
        results = (
            db.query(func.count(PatientResult.result_id))
            .filter(
                PatientResult.patient_program == ACTG_PROGRAM,
                func.date(PatientResult.run_datetime) == target_date,
            )
            .scalar()
        )
        analytes = (
            db.query(PatientResult.analyte_code)
            .filter(
                PatientResult.patient_program == ACTG_PROGRAM,
                func.date(PatientResult.run_datetime) == target_date,
            )
            .distinct()
            .all()
        )
        return {
            "date": str(target_date),
            "unique_patients": patients,
            "total_results": results,
            "analytes": [a[0] for a in analytes],
        }

    @staticmethod
    def monthly(db: Session):
        rows = (
            db.query(
                func.to_char(PatientResult.run_datetime, "YYYY-MM").label("month"),
                func.count(func.distinct(PatientResult.patient_identifier)).label("unique_patients"),
                func.count(PatientResult.result_id).label("total_results"),
                func.count(func.distinct(PatientResult.analyte_code)).label("analytes_run"),
            )
            .filter(PatientResult.patient_program == ACTG_PROGRAM)
            .group_by(func.to_char(PatientResult.run_datetime, "YYYY-MM"))
            .order_by(func.to_char(PatientResult.run_datetime, "YYYY-MM"))
            .all()
        )
        return [
            {
                "month": r.month,
                "unique_patients": r.unique_patients,
                "total_results": r.total_results,
                "analytes_run": r.analytes_run,
            }
            for r in rows
        ]

    @staticmethod
    def statistics(db: Session):
        total_patients = (
            db.query(func.count(func.distinct(PatientResult.patient_identifier)))
            .filter(PatientResult.patient_program == ACTG_PROGRAM)
            .scalar()
        )
        total_results = (
            db.query(func.count(PatientResult.result_id))
            .filter(PatientResult.patient_program == ACTG_PROGRAM)
            .scalar()
        )
        analyte_rows = (
            db.query(
                PatientResult.analyte_code,
                func.count(PatientResult.result_id).label("n"),
            )
            .filter(PatientResult.patient_program == ACTG_PROGRAM)
            .group_by(PatientResult.analyte_code)
            .order_by(func.count(PatientResult.result_id).desc())
            .all()
        )
        return {
            "total_patients": total_patients,
            "total_results": total_results,
            "analytes": [{"analyte_code": r.analyte_code, "count": r.n} for r in analyte_rows],
        }

    @staticmethod
    def export_excel(db: Session):
        rows = (
            db.query(PatientResult)
            .filter(PatientResult.patient_program == ACTG_PROGRAM)
            .order_by(PatientResult.run_datetime.desc())
            .all()
        )
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "ACTG Results"
        ws.append([
            "Result ID", "Run DateTime", "Patient ID", "Patient Initials",
            "Sample ID", "Analyte Code", "Analyte Name",
            "Result Value", "Units", "Reference Flag", "Status",
        ])
        for r in rows:
            ws.append([
                r.result_id, str(r.run_datetime), r.patient_identifier, r.patient_initials,
                r.sample_id, r.analyte_code, r.analyte_name,
                float(r.result_value) if r.result_value else None,
                r.units, r.reference_flag, r.status,
            ])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf
