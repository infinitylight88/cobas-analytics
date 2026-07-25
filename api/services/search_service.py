from sqlalchemy import or_
from sqlalchemy.orm import Session

from api.database.models import ArchiveFile, Calibration, PatientResult, QCResult


class SearchService:

    def search_sample(self, db: Session, q: str):
        term = f"%{q}%"
        rows = (
            db.query(PatientResult)
            .filter(PatientResult.sample_id.ilike(term))
            .order_by(PatientResult.run_datetime.desc())
            .limit(100)
            .all()
        )
        return [
            {
                "result_id": r.result_id,
                "sample_id": r.sample_id,
                "patient_identifier": r.patient_identifier,
                "run_datetime": str(r.run_datetime),
                "analyte_code": r.analyte_code,
            }
            for r in rows
        ]

    def search_patient(self, db: Session, q: str):
        term = f"%{q}%"
        rows = (
            db.query(PatientResult)
            .filter(
                or_(
                    PatientResult.patient_identifier.ilike(term),
                    PatientResult.patient_initials.ilike(term),
                )
            )
            .order_by(PatientResult.run_datetime.desc())
            .limit(100)
            .all()
        )
        seen = set()
        results = []
        for r in rows:
            key = r.patient_identifier
            if key not in seen:
                seen.add(key)
                results.append({
                    "patient_identifier": r.patient_identifier,
                    "patient_initials": r.patient_initials,
                    "patient_program": r.patient_program,
                    "last_seen": str(r.run_datetime),
                })
        return results

    def search_analyte(self, db: Session, q: str):
        term = f"%{q}%"
        rows = (
            db.query(
                PatientResult.analyte_code,
                PatientResult.analyte_name,
                PatientResult.assay_group,
            )
            .filter(
                or_(
                    PatientResult.analyte_code.ilike(term),
                    PatientResult.analyte_name.ilike(term),
                )
            )
            .distinct()
            .order_by(PatientResult.analyte_code)
            .all()
        )
        return [
            {"analyte_code": r.analyte_code, "analyte_name": r.analyte_name, "assay_group": r.assay_group}
            for r in rows
        ]

    def search_date(self, db: Session, q: str):
        from sqlalchemy import cast, String
        term = f"%{q}%"
        rows = (
            db.query(PatientResult)
            .filter(cast(PatientResult.run_datetime, String).ilike(term))
            .order_by(PatientResult.run_datetime.desc())
            .limit(200)
            .all()
        )
        return [
            {
                "result_id": r.result_id,
                "run_datetime": str(r.run_datetime),
                "patient_identifier": r.patient_identifier,
                "sample_id": r.sample_id,
                "analyte_code": r.analyte_code,
            }
            for r in rows
        ]

    def search_archive(self, db: Session, q: str):
        term = f"%{q}%"
        rows = (
            db.query(ArchiveFile)
            .filter(ArchiveFile.filename.ilike(term))
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
            }
            for r in rows
        ]

    def search_operator(self, db: Session, q: str):
        term = f"%{q}%"
        rows = (
            db.query(ArchiveFile)
            .filter(ArchiveFile.operator_name.ilike(term))
            .order_by(ArchiveFile.archive_start.desc())
            .all()
        )
        return [
            {
                "archive_id": r.archive_id,
                "filename": r.filename,
                "operator_name": r.operator_name,
                "archive_start": str(r.archive_start) if r.archive_start else None,
            }
            for r in rows
        ]

    def search_reagent(self, db: Session, q: str):
        term = f"%{q}%"
        cal_rows = (
            db.query(Calibration)
            .filter(Calibration.reagent_lot.ilike(term))
            .order_by(Calibration.run_datetime.desc())
            .limit(100)
            .all()
        )
        qc_rows = (
            db.query(QCResult)
            .filter(QCResult.reagent_lot.ilike(term))
            .order_by(QCResult.run_datetime.desc())
            .limit(100)
            .all()
        )
        return {
            "calibrations": [
                {"calibration_id": r.calibration_id, "analyte_code": r.analyte_code,
                 "reagent_lot": r.reagent_lot, "run_datetime": str(r.run_datetime)}
                for r in cal_rows
            ],
            "qc_results": [
                {"qc_id": r.qc_id, "analyte_code": r.analyte_code,
                 "reagent_lot": r.reagent_lot, "run_datetime": str(r.run_datetime)}
                for r in qc_rows
            ],
        }

    def search_control(self, db: Session, q: str):
        term = f"%{q}%"
        rows = (
            db.query(
                QCResult.control_name,
                QCResult.control_lot,
                QCResult.analyte_code,
            )
            .filter(QCResult.control_name.ilike(term))
            .distinct()
            .order_by(QCResult.control_name, QCResult.analyte_code)
            .all()
        )
        return [
            {"control_name": r.control_name, "control_lot": r.control_lot, "analyte_code": r.analyte_code}
            for r in rows
        ]
