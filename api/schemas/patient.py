from datetime import datetime
from pydantic import BaseModel


class PatientTestSummary(BaseModel):
    sample_id: str
    patient_identifier: str | None = None
    patient_initials: str | None = None
    patient_program: str | None = None
    run_datetime: datetime | None = None
    total_tests: int
    analytes: list[str]