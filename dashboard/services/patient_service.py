from dashboard.services.api_client import APIClient


class PatientService:

    @staticmethod
    def all():

        return APIClient.get("/patients")