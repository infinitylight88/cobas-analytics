import io
from datetime import date, datetime, timedelta
from itertools import groupby

import openpyxl
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database.models import Calibration


class CalibrationService:

    def all(self, db: Session):
        return (
            db.query(Calibration)
            .order_by(Calibration.run_datetime.desc())
            .all()
        )

    def by_date(self, db: Session, target_date: str):
        return (
            db.query(Calibration)
            .filter(func.date(Calibration.run_datetime) == date.fromisoformat(target_date))
            .order_by(Calibration.run_datetime)
            .all()
        )

    def by_analyte(self, db: Session, analyte: str):
        return (
            db.query(Calibration)
            .filter(Calibration.analyte_code == analyte)
            .order_by(Calibration.run_datetime.desc())
            .all()
        )

    def history(self, db: Session, analyte: str):
        return (
            db.query(Calibration)
            .filter(Calibration.analyte_code == analyte)
            .order_by(Calibration.run_datetime.asc())
            .all()
        )

    def get_summary(self, db: Session):
        rows = (
            db.query(Calibration)
            .order_by(Calibration.analyte_code, Calibration.run_datetime.desc())
            .all()
        )
        seen = {}
        for r in rows:
            if r.analyte_code not in seen:
                seen[r.analyte_code] = r
        counts = {
            code: n
            for code, n in (
                db.query(Calibration.analyte_code, func.count().label("n"))
                .group_by(Calibration.analyte_code)
                .all()
            )
        }
        return [
            {
                "analyte_code": code,
                "total_calibrations": counts.get(code, 0),
                "last_calibration": str(row.run_datetime),
                "calibration_type": row.calibration_type,
                "reagent_lot": row.reagent_lot,
            }
            for code, row in sorted(seen.items())
        ]

    def get_expired(self, db: Session, days: int = 30):
        cutoff = datetime.utcnow() - timedelta(days=days)
        rows = (
            db.query(Calibration)
            .order_by(Calibration.analyte_code, Calibration.run_datetime.desc())
            .all()
        )
        latest = {}
        for r in rows:
            if r.analyte_code not in latest:
                latest[r.analyte_code] = r
        result = []
        for code, r in sorted(latest.items()):
            age_days = (datetime.utcnow() - r.run_datetime).days if r.run_datetime else None
            result.append({
                "analyte_code": code,
                "last_calibration": str(r.run_datetime),
                "age_days": age_days,
                "reagent_lot": r.reagent_lot,
                "expired": age_days is not None and age_days > days,
            })
        return [r for r in result if r["expired"]]

    def by_reagent(self, db: Session, lot: str):
        return (
            db.query(Calibration)
            .filter(Calibration.reagent_lot == lot)
            .order_by(Calibration.run_datetime.desc())
            .all()
        )

    def export_excel(self, db: Session):
        rows = (
            db.query(Calibration)
            .order_by(Calibration.run_datetime.desc())
            .all()
        )
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Calibrations"
        ws.append([
            "Calibration ID", "Run DateTime", "Analyte", "Calibration Type",
            "Reagent Lot", "Slope", "Offset", "Factor",
            "Lower Limit", "Upper Limit", "Units",
        ])
        for r in rows:
            ws.append([
                r.calibration_id, str(r.run_datetime), r.analyte_code, r.calibration_type,
                r.reagent_lot,
                float(r.slope) if r.slope else None,
                float(r.offset) if r.offset else None,
                float(r.factor) if r.factor else None,
                float(r.lower_limit) if r.lower_limit else None,
                float(r.upper_limit) if r.upper_limit else None,
                r.units,
            ])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf
