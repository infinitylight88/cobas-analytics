from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ACTGPatientResult(BaseModel):

    patient_identifier: Optional[str]
    patient_initials: Optional[str]
    sample_id: Optional[str]
    analyte_code: Optional[str]
    analyte_name: Optional[str]
    result_value: Optional[float]
    units: Optional[str]
    run_datetime: Optional[datetime]


class ACTGWorkload(BaseModel):

    date: str
    unique_patients: int
    total_results: int
    analytes: list