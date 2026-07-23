from dashboard.services.api_client import APIClient


class DashboardService:

    @staticmethod
    def summary():

        return APIClient.get(
            "/dashboard/summary"
        )

    @staticmethod
    def activity():

        return APIClient.get(
            "/dashboard/activity"
        )