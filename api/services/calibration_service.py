from api.database.session import SessionLocal
from api.database.models import Calibration
from sqlalchemy import func


class CalibrationService:

    @staticmethod
    def all():

        db = SessionLocal()

        try:

            return db.query(
                Calibration
            ).order_by(
                Calibration.run_datetime.desc()
            ).all()

        finally:

            db.close()

    @staticmethod
    def by_date(target_date):

        db = SessionLocal()

        try:

            return (
                db.query(Calibration)
                .filter(func.date(Calibration.run_datetime) == target_date)
                .all()
            )

        finally:
            db.close()

    @staticmethod
    def by_analyte(analyte):

        db = SessionLocal()

        try:

            return (
                db.query(Calibration)
                .filter(Calibration.analyte_code == analyte)
                .order_by(Calibration.run_datetime.desc())
                .all()
            )

        finally:
            db.close()

    @staticmethod
    def summary():

        db = SessionLocal()

        try:

            return (
                db.query(
                    Calibration.analyte_code,
                    func.count().label("calibrations")
                )
                .group_by(Calibration.analyte_code)
                .order_by(func.count().desc())
                .all()
            )

        finally:
            db.close()