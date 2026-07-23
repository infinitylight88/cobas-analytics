from database.patient_writer import PatientWriter
from database.qc_writer import QCWriter
from database.calibration_writer import CalibrationWriter
from database.host_writer import HostWriter
from database.maintenance_writer import MaintenanceWriter
from parser.cobas_rules import CobasRules


class ActivityClassifier:
    """
    All Cobas business rules live here.

    Record code alone never decides where data goes.
    The contents of the record decide.
    """

    PATIENT_ANALYTES_IN_RECORD50 = {
        "RWD3",
        "BUN",
        "BUN2",
        "BUNJ2"
    }

    HBA1C_COMPONENTS = {
        "HB-W3",
        "A1-W3",
        "RWD3"
    }

    @staticmethod
    def process(archive_id, raw_id, fields):
        if not fields:
            return

        record = fields[0]
        analyte = fields[2].strip().upper() if len(fields) > 2 else ""

        # -------------------------
        # Calibration
        # -------------------------
        if record == "10":
            CalibrationWriter.write(
                archive_id,
                raw_id,
                fields
            )
            return

        # -------------------------
        # QC
        # -------------------------
        if record == "20":
            QCWriter.write(
                archive_id,
                raw_id,
                fields
            )
            return

        # -------------------------
        # Maintenance
        # -------------------------
        if record == "30":
            MaintenanceWriter.write(
                archive_id,
                raw_id,
                fields
            )
            return

        # -------------------------
        # Normal patient results
        # -------------------------
        if record == "40":
            # 1. Initialize default values
            activity_type = "PATIENT"
            assay_group = "CHEMISTRY"
            qc_level = None

            # 2. Sanitize and transform the analyte key name
            analyte = analyte.upper()

            # 3. Classify the diagnostic group using external CobasRules configuration
            if analyte in CobasRules.HBA1C_ANALYTES:
                assay_group = "HBA1C"
            else:
                assay_group = "CHEMISTRY"

            # 4. Check special import conditions (Field 3 is Control, Field 4 is QC Level)
            if len(fields) > 4:
                if fields[3].strip().upper() == "CONTROL":
                    activity_type = "QC"
                    qc_level = fields[4].strip().upper()

            # 5. Commit record to database using the newly assigned markers
            PatientWriter.write(
                archive_id,
                raw_id,
                fields,
                activity_type,
                assay_group,
                qc_level
            )
            return

        # -------------------------
        # Record 50 can contain
        #
        #   • BUN
        #   • HbA1c RWD3
        #   • Host Events
        #
        # Decide using analyte.
        # -------------------------
        if record == "50":
            if analyte in ActivityClassifier.PATIENT_ANALYTES_IN_RECORD50:
                PatientWriter.write(
                    archive_id,
                    raw_id,
                    fields,
                    "PATIENT",      # activity_type fallback
                    "CHEMISTRY",    # assay_group fallback
                    None            # qc_level fallback
                )
            else:
                HostWriter.write(
                    archive_id,
                    raw_id,
                    fields
                )
            return

