class Normalizer:

    @staticmethod
    def clean(value):

        if value is None:
            return None

        value = value.strip()

        if value == "":
            return None

        if value.upper() == "UNDEFINED":
            return None

        return value

    @staticmethod
    def patient(fields):

        """
        Converts raw archive fields into a clean dictionary.
        """

        field3 = Normalizer.clean(fields[3])
        field4 = Normalizer.clean(fields[4])
        field5 = Normalizer.clean(fields[5])

        initials = None
        patient_id = None
        accession = None
        source = None
        control_level = None

        # ------------------------
        # Controls
        # ------------------------

        if field3 == "CONTROL":

            source = "CONTROL"
            control_level = field4

        # ------------------------
        # ACTG
        # ------------------------

        elif field4 and field4.startswith("124"):

            source = "ACTG"

            patient_id = field4

            if field3 and field3.startswith("PT INITIALS:"):

                initials = field3.replace(
                    "PT INITIALS:",
                    ""
                ).strip()

        # ------------------------
        # LIMS accession
        # ------------------------

        elif field5 and field5.startswith("133"):

            source = "LIMS"

            accession = field5

        # ------------------------
        # JCMB
        # ------------------------

        elif field5 and "JCMB" in field5.upper():

            source = "JCMB"

            accession = field5

            patient_id = field4

        # ------------------------

        return {

            "record_code": int(fields[0]),

            "result_datetime": fields[1],

            "test_code": fields[2],

            "patient_initials": initials,

            "patient_id": patient_id,

            "accession_number": accession,

            "patient_source": source,

            "control_level": control_level,

            "sample_type": Normalizer.clean(fields[6]),

            "units": Normalizer.clean(fields[7]),

            "flag": Normalizer.clean(fields[8]),

            "result": Normalizer.clean(fields[10]),

            "gender": Normalizer.clean(fields[13]),

            "dob": Normalizer.clean(fields[14])

        }