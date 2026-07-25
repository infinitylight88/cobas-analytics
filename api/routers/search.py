from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.session import get_db
from api.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])
service = SearchService()


@router.get("/sample")
def search_sample(q: str, db: Session = Depends(get_db)):
    return service.search_sample(db, q)


@router.get("/patient")
def search_patient(q: str, db: Session = Depends(get_db)):
    return service.search_patient(db, q)


@router.get("/analyte")
def search_analyte(q: str, db: Session = Depends(get_db)):
    return service.search_analyte(db, q)


@router.get("/date")
def search_date(q: str, db: Session = Depends(get_db)):
    return service.search_date(db, q)


@router.get("/archive")
def search_archive(q: str, db: Session = Depends(get_db)):
    return service.search_archive(db, q)


@router.get("/operator")
def search_operator(q: str, db: Session = Depends(get_db)):
    return service.search_operator(db, q)


@router.get("/reagent")
def search_reagent(q: str, db: Session = Depends(get_db)):
    return service.search_reagent(db, q)


@router.get("/control")
def search_control(q: str, db: Session = Depends(get_db)):
    return service.search_control(db, q)
