from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from api.routers.system import router as system_router
from api.routers.archive import router as archive_router
from api.routers import dashboard
from api.routers import patients
from api.routers import calibrations
from api.routers import actg
from api.routers import analytes
from api.routers import qc
from api.routers import hba1c
from api.routers import audit
from api.routers import reports
from api.routers import search

app = FastAPI(
    title="Cobas Integra Analytics API",
    version="1.0.0",
    description="Laboratory analytics platform for the Roche Cobas Integra 400 Plus Clinical Chemistry Analyzer.",
)

app.include_router(system_router)
app.include_router(archive_router)
app.include_router(dashboard.router)
app.include_router(patients.router)
app.include_router(calibrations.router)
app.include_router(actg.router)
app.include_router(analytes.router)
app.include_router(qc.router)
app.include_router(hba1c.router)
app.include_router(audit.router)
app.include_router(reports.router)
app.include_router(search.router)

# Serve the browser dashboard
app.mount("/static", StaticFiles(directory="api/static"), name="static")


@app.get("/ui", include_in_schema=False)
def ui_dashboard():
    return FileResponse("api/static/index.html")


@app.get("/")
def root():
    return RedirectResponse(url="/ui")
