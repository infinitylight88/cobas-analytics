from fastapi import APIRouter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/actg")
def actg():

    return [
        {
            "study": "ACTG",
            "samples": 0,
            "hba1c": 0,
            "latest_run": "-"
        }
    ]


@router.get("/hba1c")
def hba1c():

    return []


@router.get("/workload")
def workload():

    return []