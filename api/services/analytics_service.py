from sqlalchemy import func

from api.database.session import SessionLocal
from api.database.models import PatientResult


class AnalyticsService:

    @staticmethod
    def workload():

        db = SessionLocal()

        try:

            return (
                db.query(
                    PatientResult.run_datetime,
                    func.count(PatientResult.result_id)
                )
                .group_by(
                    PatientResult.run_datetime
                )
                .order_by(
                    PatientResult.run_datetime
                )
                .all()
            )

        finally:

            db.close()