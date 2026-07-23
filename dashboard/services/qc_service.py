from dashboard.services.api_client import APIClient


class QCService:

    @staticmethod
    def all():

        return APIClient.get("/qc")