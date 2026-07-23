from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Text
)

from .base import Base


class ArchiveFile(Base):

    __tablename__ = "archive_files"

    archive_id = Column(Integer, primary_key=True)

    filename = Column(Text)

    archive_start = Column(Date)

    archive_end = Column(Date)

    instrument_id = Column(Integer)

    operator_name = Column(String)

    archive_version = Column(String)

    imported_at = Column(DateTime)

from sqlalchemy import Date


class Patient(Base):

    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True)

    patient_identifier = Column(String)

    patient_initials = Column(String)

    patient_program = Column(String)

    sex = Column(String)

    date_of_birth = Column(Date)

from sqlalchemy import Numeric


class PatientResult(Base):

    __tablename__ = "patient_results"

    result_id = Column(Integer, primary_key=True)

    archive_id = Column(Integer)

    patient_id = Column(Integer)

    raw_id = Column(Integer)

    run_datetime = Column(DateTime)

    sample_id = Column(String)

    sample_type = Column(String)

    analyte_code = Column(String)

    analyte_name = Column(String)

    result_value = Column(Numeric)

    units = Column(String)

    reference_flag = Column(String)

    status = Column(String)

    result_flag = Column(String)

    activity_type = Column(String)

    assay_group = Column(String)

    qc_level = Column(String)

    patient_program = Column(String)

    instrument_position = Column(String)

    patient_initials = Column(String)

    patient_identifier = Column(String)

class QCResult(Base):

    __tablename__ = "qc_results"

    qc_id = Column(Integer, primary_key=True)

    archive_id = Column(Integer)

    raw_id = Column(Integer)

    run_datetime = Column(DateTime)

    analyte_code = Column(String)

    control_name = Column(String)

    control_lot = Column(String)

    units = Column(String)

    assigned_value = Column(Numeric)

    measured_value = Column(Numeric)

    sd = Column(Numeric)

    lower_limit = Column(Numeric)

    upper_limit = Column(Numeric)

    activity_type = Column(String)

    assay_group = Column(String)

    qc_level = Column(String)

    application_code = Column(String)

    reagent_lot = Column(String)

    instrument_signal = Column(Numeric)

class Calibration(Base):

    __tablename__ = "calibrations"

    calibration_id = Column(Integer, primary_key=True)

    archive_id = Column(Integer)

    raw_id = Column(Integer)

    run_datetime = Column(DateTime)

    analyte_code = Column(String)

    calibration_type = Column(String)

    reagent_lot = Column(String)

    units = Column(String)

    upper_limit = Column(Numeric)

    lower_limit = Column(Numeric)

    slope = Column(Numeric)

    offset = Column(Numeric)

    factor = Column(Numeric)

    activity_type = Column(String)

    assay_group = Column(String)

class RawRecord(Base):

    __tablename__ = "raw_records"

    raw_id = Column(Integer, primary_key=True)

    archive_id = Column(Integer)

    line_number = Column(Integer)

    record_code = Column(Integer)

    raw_text = Column(Text)