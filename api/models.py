from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import DateTime

from api.database import Base


class PatientResult(Base):

    __tablename__ = "patient_results"

    result_id = Column(Integer, primary_key=True)

    run_datetime = Column(DateTime)

    sample_id = Column(String)

    analyte_code = Column(String)

    result_value = Column(Numeric)

    units = Column(String)

    activity_type = Column(String)

    assay_group = Column(String)

    qc_level = Column(String)

class Calibration(Base):

    __tablename__ = "calibrations"

    calibration_id = Column(Integer, primary_key=True)