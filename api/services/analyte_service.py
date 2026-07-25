from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database.models import PatientResult, QCResult

# Electrolyte analyte codes measured by ISE (Ion Selective Electrode)
ISE_CODES = {"CL-I", "K-I", "NA-I", "CO2-L"}


class AnalyteService:

    def get_all(self, db: Session):
        rows = (
            db.query(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                PatientResult.assay_group,
                func.count(PatientResult.result_id).label("result_count"),
            )
            .group_by(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                PatientResult.assay_group,
            )
            .order_by(PatientResult.assay_group, PatientResult.analyte_code)
            .all()
        )
        return [
            {
                "analyte_code": r.analyte_code,
                "analyte_name": r.analyte_name,
                "assay_group": r.assay_group,
                "result_count": r.result_count,
            }
            for r in rows
        ]

    def get_by_code(self, db: Session, analyte: str):
        return (
            db.query(PatientResult)
            .filter(PatientResult.analyte_code == analyte)
            .order_by(PatientResult.run_datetime.desc())
            .all()
        )

    def get_chemistry(self, db: Session):
        rows = (
            db.query(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                func.count(PatientResult.result_id).label("result_count"),
            )
            .filter(
                PatientResult.assay_group == "CHEMISTRY",
                PatientResult.analyte_code.notin_(ISE_CODES),
            )
            .group_by(PatientResult.analyte_code, PatientResult.analyte_name)
            .order_by(PatientResult.analyte_code)
            .all()
        )
        return [
            {"analyte_code": r.analyte_code, "analyte_name": r.analyte_name, "result_count": r.result_count}
            for r in rows
        ]

    def get_hba1c(self, db: Session):
        rows = (
            db.query(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                func.count(PatientResult.result_id).label("result_count"),
            )
            .filter(PatientResult.assay_group == "HBA1C")
            .group_by(PatientResult.analyte_code, PatientResult.analyte_name)
            .order_by(PatientResult.analyte_code)
            .all()
        )
        return [
            {"analyte_code": r.analyte_code, "analyte_name": r.analyte_name, "result_count": r.result_count}
            for r in rows
        ]

    def get_ise(self, db: Session):
        rows = (
            db.query(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                func.count(PatientResult.result_id).label("result_count"),
            )
            .filter(PatientResult.analyte_code.in_(ISE_CODES))
            .group_by(PatientResult.analyte_code, PatientResult.analyte_name)
            .order_by(PatientResult.analyte_code)
            .all()
        )
        return [
            {"analyte_code": r.analyte_code, "analyte_name": r.analyte_name, "result_count": r.result_count}
            for r in rows
        ]

    def get_summary(self, db: Session):
        rows = (
            db.query(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                PatientResult.assay_group,
                func.count(PatientResult.result_id).label("total_results"),
                func.count(func.distinct(PatientResult.patient_identifier)).label("unique_patients"),
                func.min(PatientResult.run_datetime).label("first_run"),
                func.max(PatientResult.run_datetime).label("last_run"),
            )
            .group_by(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                PatientResult.assay_group,
            )
            .order_by(PatientResult.assay_group, func.count(PatientResult.result_id).desc())
            .all()
        )
        return [
            {
                "analyte_code": r.analyte_code,
                "analyte_name": r.analyte_name,
                "assay_group": r.assay_group,
                "total_results": r.total_results,
                "unique_patients": r.unique_patients,
                "first_run": str(r.first_run),
                "last_run": str(r.last_run),
            }
            for r in rows
        ]
