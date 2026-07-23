from dashboard.services.api_client import APIClient


class AnalyticsService:

    @staticmethod
    def actg():

        return APIClient.get(
            "/analytics/actg"
        )

    @staticmethod
    def hba1c():

        return APIClient.get(
            "/analytics/hba1c"
        )

    @staticmethod
    def workload():

        return APIClient.get(
            "/analytics/workload"
        )