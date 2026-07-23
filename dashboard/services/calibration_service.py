from dashboard.services.api_client import APIClient


class CalibrationService:

    @staticmethod
    def all():

        return APIClient.get("/calibrations")