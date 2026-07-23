from sqlalchemy.orm import Session
from api.database.session import SessionLocal
from api.database.models import PatientResult

class PatientService:

    @staticmethod
    def all():

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).order_by(
                PatientResult.run_datetime.desc()
            ).all()

        finally:

            db.close()

    @staticmethod
    def sample(sample_id):

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.sample_id == sample_id
            ).all()

        finally:

            db.close()

    @staticmethod
    def sample(sample_id):

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.sample_id == sample_id
            ).all()

        finally:

            db.close()

    @staticmethod
    def activity(activity):

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.activity_type == activity
            ).all()

        finally:

            db.close()

    @staticmethod
    def assay(name):

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.assay_group == name
            ).all()

        finally:

            db.close()

    @staticmethod
    def qc_level(level):

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.qc_level == level
            ).all()

        finally:

            db.close()

    @staticmethod
    def actg():

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.activity_type == "ACTG"
            ).all()

        finally:

            db.close()

    @staticmethod
    def lims():

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.activity_type == "LIMS"
            ).all()

        finally:

            db.close()

    @staticmethod
    def hba1c_controls():

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.assay_group == "HBA1C",
                PatientResult.activity_type == "QC"
            ).order_by(
                PatientResult.run_datetime.desc()
            ).all()

        finally:

            db.close()

    @staticmethod
    def bun():

        db = SessionLocal()

        try:

            return db.query(
                PatientResult
            ).filter(
                PatientResult.analyte_code == "BUN"
            ).all()

        finally:

            db.close()

    @staticmethod
    def get_tests_per_patient(
        db: Session,
        sample_id: str
    ):

        rows = (
            db.query(PatientResult)
            .filter(
                PatientResult.sample_id == sample_id
            )
            .order_by(
                PatientResult.analyte_code
            )
            .all()
        )

        if not rows:
            return None

        first = rows[0]

        analytes = sorted(
            {
                r.analyte_code
                for r in rows
                if r.analyte_code
            }
        )

        return {
            "sample_id": first.sample_id,
            "patient_identifier": first.patient_identifier,
            "patient_initials": first.patient_initials,
            "patient_program": first.patient_program,
            "run_datetime": first.run_datetime,
            "total_tests": len(rows),
            "analytes": analytes
        }