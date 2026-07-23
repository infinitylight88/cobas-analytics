from datetime import datetime

from decimal import Decimal

from pydantic import BaseModel


class PatientResultSchema(BaseModel):

    result_id:int

    run_datetime:datetime

    sample_id:str | None

    analyte_code:str | None

    result_value:Decimal | None

    units:str | None

    activity_type:str | None

    assay_group:str | None

    qc_level:str | None

    class Config:

        from_attributes = True