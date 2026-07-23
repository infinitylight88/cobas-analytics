from sqlalchemy import func

from api.database.models import PatientResult, Patient


class ACTGService:


    @staticmethod
    def patients(db):

        return (
            db.query(Patient)
            .filter(
                Patient.patient_program=="ACTG"
            )
            .all()
        )


    @staticmethod
    def patient_results(db, patient_id):

        return (

            db.query(
                PatientResult
            )
            .filter(
                PatientResult.patient_identifier==patient_id
            )
            .order_by(
                PatientResult.run_datetime.desc()
            )
            .all()

        )


    @staticmethod
    def workload(db, target_date):


        patients = (
            db.query(
                func.count(
                    func.distinct(
                        PatientResult.patient_identifier
                    )
                )
            )
            .filter(
                PatientResult.patient_program=="ACTG",
                func.date(
                    PatientResult.run_datetime
                ) == target_date
            )
            .scalar()
        )


        results = (
            db.query(
                func.count(
                    PatientResult.result_id
                )
            )
            .filter(
                PatientResult.patient_program=="ACTG",
                func.date(
                    PatientResult.run_datetime
                ) == target_date
            )
            .scalar()
        )


        analytes = (

            db.query(
                PatientResult.analyte_code
            )
            .filter(
                PatientResult.patient_program=="ACTG",
                func.date(
                    PatientResult.run_datetime
                ) == target_date
            )
            .distinct()
            .all()

        )


        return {

            "date": str(target_date),

            "unique_patients": patients,

            "total_results": results,

            "analytes":[
                a[0] for a in analytes
            ]

        }