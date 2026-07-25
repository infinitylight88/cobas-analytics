from datetime import date

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from api.database.models import Patient, PatientResult


class PatientService:

    def all(self, db: Session):
        return (
            db.query(PatientResult)
            .order_by(PatientResult.run_datetime.desc())
            .all()
        )

    def by_identifier(self, db: Session, patient_identifier: str):
        return (
            db.query(PatientResult)
            .filter(PatientResult.patient_identifier == patient_identifier)
            .order_by(PatientResult.run_datetime.desc())
            .all()
        )

    def by_sample(self, db: Session, sample_id: str):
        return (
            db.query(PatientResult)
            .filter(PatientResult.sample_id == sample_id)
            .all()
        )

    def get_tests_per_patient(self, db: Session, sample_id: str):
        rows = (
            db.query(PatientResult)
            .filter(PatientResult.sample_id == sample_id)
            .order_by(PatientResult.analyte_code)
            .all()
        )
        if not rows:
            return None
        first = rows[0]
        analytes = sorted({r.analyte_code for r in rows if r.analyte_code})
        return {
            "sample_id": first.sample_id,
            "patient_identifier": first.patient_identifier,
            "patient_initials": first.patient_initials,
            "patient_program": first.patient_program,
            "run_datetime": first.run_datetime,
            "total_tests": len(rows),
            "analytes": analytes,
        }

    def get_history(self, db: Session, patient_identifier: str):
        rows = (
            db.query(PatientResult)
            .filter(PatientResult.patient_identifier == patient_identifier)
            .order_by(PatientResult.run_datetime.desc())
            .all()
        )
        if not rows:
            return None
        analytes = sorted({r.analyte_code for r in rows if r.analyte_code})
        visits = {}
        for r in rows:
            d = str(func.date(r.run_datetime)) if r.run_datetime else None
            d = str(r.run_datetime.date()) if r.run_datetime else None
            if d not in visits:
                visits[d] = 0
            visits[d] += 1
        return {
            "patient_identifier": patient_identifier,
            "patient_initials": rows[0].patient_initials,
            "patient_program": rows[0].patient_program,
            "total_results": len(rows),
            "analytes": analytes,
            "results": [
                {
                    "result_id": r.result_id,
                    "run_datetime": str(r.run_datetime),
                    "sample_id": r.sample_id,
                    "analyte_code": r.analyte_code,
                    "analyte_name": r.analyte_name,
                    "result_value": float(r.result_value) if r.result_value is not None else None,
                    "units": r.units,
                    "reference_flag": r.reference_flag,
                    "status": r.status,
                }
                for r in rows
            ],
        }

    def by_day(self, db: Session, target_date: str):
        d = date.fromisoformat(target_date)
        rows = (
            db.query(
                PatientResult.patient_identifier,
                PatientResult.patient_initials,
                PatientResult.patient_program,
                func.count(PatientResult.result_id).label("tests"),
                func.count(func.distinct(PatientResult.sample_id)).label("samples"),
            )
            .filter(func.date(PatientResult.run_datetime) == d)
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
                "samples": r.samples,
            }
            for r in rows
        ]

    def search(self, db: Session, q: str):
        term = f"%{q}%"
        rows = (
            db.query(PatientResult)
            .filter(
                or_(
                    PatientResult.patient_identifier.ilike(term),
                    PatientResult.patient_initials.ilike(term),
                    PatientResult.sample_id.ilike(term),
                )
            )
            .order_by(PatientResult.run_datetime.desc())
            .limit(200)
            .all()
        )
        return rows

    def get_analytes(self, db: Session, patient_identifier: str):
        rows = (
            db.query(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                PatientResult.assay_group,
                func.count(PatientResult.result_id).label("count"),
                func.min(PatientResult.run_datetime).label("first_run"),
                func.max(PatientResult.run_datetime).label("last_run"),
            )
            .filter(PatientResult.patient_identifier == patient_identifier)
            .group_by(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                PatientResult.assay_group,
            )
            .order_by(PatientResult.analyte_code)
            .all()
        )
        return [
            {
                "analyte_code": r.analyte_code,
                "analyte_name": r.analyte_name,
                "assay_group": r.assay_group,
                "count": r.count,
                "first_run": str(r.first_run),
                "last_run": str(r.last_run),
            }
            for r in rows
        ]
