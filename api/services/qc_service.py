from sqlalchemy import func

from api.database.session import SessionLocal
from api.database.models import QCResult, PatientResult


class QCService:

    @staticmethod
    def all():

        db = SessionLocal()

        try:

            return (
                db.query(QCResult)
                .order_by(QCResult.run_datetime.desc())
                .all()
            )

        finally:
            db.close()

    @staticmethod
    def get_by_date(target_date):

        db = SessionLocal()

        try:

            return (
                db.query(QCResult)
                .filter(
                    func.date(QCResult.run_datetime) == target_date
                )
                .order_by(QCResult.run_datetime)
                .all()
            )

        finally:
            db.close()

    @staticmethod
    def get_by_analyte(analyte):

        db = SessionLocal()

        try:

            return (
                db.query(QCResult)
                .filter(
                    QCResult.analyte_code == analyte
                )
                .order_by(QCResult.run_datetime.desc())
                .all()
            )

        finally:
            db.close()

    @staticmethod
    def get_summary():

        db = SessionLocal()

        try:

            return (
                db.query(
                    QCResult.analyte_code,
                    func.count().label("runs")
                )
                .group_by(QCResult.analyte_code)
                .order_by(func.count().desc())
                .all()
            )

        finally:
            db.close()

    @staticmethod
    def get_compliance(db, target_date):

        patient = {
            r[0]
            for r in (
                db.query(PatientResult.analyte_code)
                .filter(
                    func.date(PatientResult.run_datetime) == target_date
                )
                .distinct()
                .all()
            )
        }

        qc = {
            r[0]
            for r in (
                db.query(QCResult.analyte_code)
                .filter(
                    func.date(QCResult.run_datetime) == target_date
                )
                .distinct()
                .all()
            )
        }

        if not patient:

            return {
                "date": target_date,
                "required": 0,
                "performed": 0,
                "missing": 0,
                "compliance": 100
            }

        performed = len(patient & qc)

        required = len(patient)

        return {

            "date": target_date,

            "required": required,

            "performed": performed,

            "missing": required - performed,

            "compliance": round(
                performed * 100 / required,
                2
            )
        }

    @staticmethod
    def get_missing(db, target_date):

        # -----------------------------------------
        # analytes that actually had patient tests
        # -----------------------------------------

        patient_analytes = {
            row[0]
            for row in (
                db.query(
                    PatientResult.analyte_code
                )
                .filter(
                    func.date(PatientResult.run_datetime) == target_date
                )
                .distinct()
                .all()
            )
        }

        # -----------------------------------------
        # analytes with QC
        # -----------------------------------------

        qc_analytes = {
            row[0]
            for row in (
                db.query(
                    QCResult.analyte_code
                )
                .filter(
                    func.date(QCResult.run_datetime) == target_date
                )
                .distinct()
                .all()
            )
        }

        # -----------------------------------------

        missing = sorted(
            patient_analytes - qc_analytes
        )

        return [
            {
                "analyte": analyte,
                "status": "Missing QC"
            }
            for analyte in missing
        ]