from sqlalchemy import func

from api.database import SessionLocal
from api.database.models import PatientResult
from api.database.models import Calibration
from api.database.models import QCResult
from api.database.models import ArchiveFile
from sqlalchemy.orm import Session
from api.database.models import PatientResult


class DashboardService:

    @staticmethod
    def summary():

        db = SessionLocal()

        return {

            "patients":
                db.query(PatientResult).count(),

            "qc":
                db.query(QCResult).count(),

            "calibrations":
                db.query(Calibration).count(),

            "archives":
                db.query(ArchiveFile).count()

        }


    @staticmethod
    def activity():

        db = SessionLocal()

        rows = (

            db.query(

                func.date(PatientResult.run_datetime).label("date"),

                func.count(PatientResult.result_id).label("patients")

            )

            .group_by(func.date(PatientResult.run_datetime))

            .order_by(func.date(PatientResult.run_datetime).desc())

            .limit(20)

            .all()

        )

        output = []

        for row in rows:

            output.append({

                "date": str(row.date),

                "patients": row.patients,

                "qc": 0,

                "calibrations": 0,

                "archives": 0

            })

        return output


    @staticmethod
    def daily_workload(
        db: Session,
        target_date
    ):

        result = (
            db.query(
                func.count(
                    func.distinct(
                        PatientResult.sample_id
                    )
                )
                .label("samples")
            )
            .filter(
                func.date(
                    PatientResult.run_datetime
                ) == target_date
            )
            .first()
        )


        return {
            "date": target_date,
            "unique_samples": result.samples or 0
        }

    @staticmethod
    def analytes_run_on_date(db, target_date):

        return (
            db.query(
                PatientResult.analyte_code
            )
            .filter(
                func.date(PatientResult.run_datetime) == target_date
            )
            .distinct()
            .all()
        )