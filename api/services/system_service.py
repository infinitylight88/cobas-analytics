from sqlalchemy import func

from api.services.base_service import BaseService
from api.database.models import (
    ArchiveFile,
    Patient,
    PatientResult,
    QCResult,
    Calibration,
    RawRecord,
)


class SystemService(BaseService):

    def status(self):

        return {
            "database": "Connected",

            "archives":
                self.db.query(func.count(ArchiveFile.archive_id)).scalar(),

            "raw_records":
                self.db.query(func.count(RawRecord.raw_id)).scalar(),

            "patients":
                self.db.query(func.count(Patient.patient_id)).scalar(),

            "patient_results":
                self.db.query(func.count(PatientResult.result_id)).scalar(),

            "qc_results":
                self.db.query(func.count(QCResult.qc_id)).scalar(),

            "calibrations":
                self.db.query(func.count(Calibration.calibration_id)).scalar()
        }