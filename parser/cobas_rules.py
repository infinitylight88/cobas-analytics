"""
Cobas business rules.

This file contains ONLY laboratory rules.

If another Cobas archive is imported in future,
only this file should need updating.
"""


class CobasRules:

    # -------------------------------------------------------
    # HbA1c analytes
    # -------------------------------------------------------

    HBA1C_ANALYTES = {
        "HB-W3",
        "A1-W3",
        "RWD3"
    }

    # -------------------------------------------------------
    # HbA1c control levels
    # -------------------------------------------------------

    HBA1C_CONTROLS = {
        "NORMAL",
        "PATHOLOGICAL"
    }

    # -------------------------------------------------------
    # Patient ID prefixes
    # -------------------------------------------------------

    ACTG_PATIENT_PREFIX = "124"

    # Examples:
    # 1332018-B
    # 1331747-W
    # JCMB001223

    ACCESSION_PREFIXES = (
        "133",
        "JCMB"
    )

    # -------------------------------------------------------
    # Record 50 patient analytes
    # -------------------------------------------------------

    RECORD50_PATIENT_ANALYTES = {
        "RWD3",
        "BUN",
        "BUN2",
        "BUNJ2"
    }

    # -------------------------------------------------------
    # Record identifiers
    # -------------------------------------------------------

    RECORD_CALIBRATION = "10"

    RECORD_QC = "20"

    RECORD_MAINTENANCE = "30"

    RECORD_PATIENT = "40"

    RECORD_SPECIAL = "50"