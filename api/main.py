from fastapi import FastAPI

from api.routers.system import router as system_router
from api.routers.system import router as system_router
from api.routers.archive import router as archive_router
from api.routers import dashboard
from api.routers import patients
from api.routers import calibrations
from api.routers import actg




app = FastAPI(
    title="Cobas Integra Analytics API",
    version="1.0.0"
)

app.include_router(system_router)

app.include_router(archive_router)

app.include_router(dashboard.router)

app.include_router(patients.router)

app.include_router(calibrations.router)

app.include_router(actg.router)


@app.get("/")
def root():

    return {
        "application": "Cobas Integra Analytics API",
        "status": "Running"
    }