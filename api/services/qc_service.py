import io
import statistics
from datetime import date
from itertools import groupby

import openpyxl
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database.models import PatientResult, QCResult


class QCService:

    def get_by_date(self, db: Session, target_date: str):
        return (
            db.query(QCResult)
            .filter(func.date(QCResult.run_datetime) == date.fromisoformat(target_date))
            .order_by(QCResult.run_datetime)
            .all()
        )

    def get_by_analyte(self, db: Session, analyte: str):
        return (
            db.query(QCResult)
            .filter(QCResult.analyte_code == analyte)
            .order_by(QCResult.run_datetime.desc())
            .all()
        )

    def get_summary(self, db: Session):
        rows = (
            db.query(QCResult.analyte_code, func.count().label("runs"))
            .group_by(QCResult.analyte_code)
            .order_by(func.count().desc())
            .all()
        )
        return [{"analyte_code": r.analyte_code, "runs": r.runs} for r in rows]

    def get_compliance(self, db: Session, target_date: str):
        d = date.fromisoformat(target_date)
        patient = {
            r[0] for r in
            db.query(PatientResult.analyte_code)
            .filter(func.date(PatientResult.run_datetime) == d)
            .distinct().all()
        }
        qc = {
            r[0] for r in
            db.query(QCResult.analyte_code)
            .filter(func.date(QCResult.run_datetime) == d)
            .distinct().all()
        }
        if not patient:
            return {"date": target_date, "required": 0, "performed": 0, "missing": 0, "compliance_pct": 100}
        performed = len(patient & qc)
        required = len(patient)
        return {
            "date": target_date,
            "required": required,
            "performed": performed,
            "missing": required - performed,
            "compliance_pct": round(performed * 100 / required, 2),
        }

    def get_missing(self, db: Session, target_date: str):
        d = date.fromisoformat(target_date)
        patient_analytes = {
            r[0] for r in
            db.query(PatientResult.analyte_code)
            .filter(func.date(PatientResult.run_datetime) == d)
            .distinct().all()
        }
        qc_analytes = {
            r[0] for r in
            db.query(QCResult.analyte_code)
            .filter(func.date(QCResult.run_datetime) == d)
            .distinct().all()
        }
        return [{"analyte": a, "status": "Missing QC"} for a in sorted(patient_analytes - qc_analytes)]

    def get_history(self, db: Session, analyte: str):
        return (
            db.query(QCResult)
            .filter(QCResult.analyte_code == analyte)
            .order_by(QCResult.run_datetime.asc())
            .all()
        )

    def get_by_control(self, db: Session, control_name: str):
        return (
            db.query(QCResult)
            .filter(QCResult.control_name == control_name)
            .order_by(QCResult.run_datetime.desc())
            .all()
        )

    def get_by_lot(self, db: Session, lot: str):
        return (
            db.query(QCResult)
            .filter(QCResult.control_lot == lot)
            .order_by(QCResult.run_datetime.desc())
            .all()
        )

    def get_statistics(self, db: Session):
        rows = (
            db.query(QCResult)
            .order_by(QCResult.analyte_code, QCResult.control_name, QCResult.control_lot)
            .all()
        )
        results = []
        key_fn = lambda r: (r.analyte_code, r.control_name, r.control_lot)
        for key, grp in groupby(rows, key=key_fn):
            grp = list(grp)
            measured = [float(r.measured_value) for r in grp if r.measured_value is not None]
            n = len(measured)
            if n == 0:
                continue
            mean_m = sum(measured) / n
            sd_m = statistics.stdev(measured) if n > 1 else 0.0
            assigned = float(grp[0].assigned_value) if grp[0].assigned_value else None
            cv = round(sd_m / mean_m * 100, 2) if mean_m else 0.0
            bias = round((mean_m - assigned) / assigned * 100, 2) if assigned else None
            results.append({
                "analyte_code": key[0],
                "control_name": key[1],
                "control_lot": key[2],
                "n": n,
                "assigned_value": assigned,
                "mean_measured": round(mean_m, 4),
                "sd_measured": round(sd_m, 4),
                "cv_pct": cv,
                "bias_pct": bias,
            })
        return results

    def get_outliers(self, db: Session):
        rows = (
            db.query(QCResult)
            .filter(
                QCResult.sd.isnot(None),
                QCResult.sd > 0,
                QCResult.measured_value.isnot(None),
                QCResult.assigned_value.isnot(None),
            )
            .all()
        )
        outliers = []
        for r in rows:
            sd = float(r.sd)
            measured = float(r.measured_value)
            assigned = float(r.assigned_value)
            z = (measured - assigned) / sd
            if abs(z) > 3:
                outliers.append({
                    "qc_id": r.qc_id,
                    "analyte_code": r.analyte_code,
                    "control_name": r.control_name,
                    "control_lot": r.control_lot,
                    "run_datetime": str(r.run_datetime),
                    "measured_value": measured,
                    "assigned_value": assigned,
                    "sd": sd,
                    "z_score": round(z, 2),
                })
        return outliers

    def get_levy_jennings(self, db: Session, analyte: str):
        rows = (
            db.query(QCResult)
            .filter(QCResult.analyte_code == analyte)
            .order_by(QCResult.run_datetime.asc())
            .all()
        )
        result = []
        for r in rows:
            z = within_2sd = within_3sd = None
            if r.sd and float(r.sd) > 0 and r.measured_value is not None and r.assigned_value is not None:
                z = round(float((r.measured_value - r.assigned_value) / r.sd), 2)
                within_2sd = abs(z) <= 2
                within_3sd = abs(z) <= 3
            result.append({
                "qc_id": r.qc_id,
                "run_datetime": str(r.run_datetime),
                "control_name": r.control_name,
                "control_lot": r.control_lot,
                "measured_value": float(r.measured_value) if r.measured_value is not None else None,
                "assigned_value": float(r.assigned_value) if r.assigned_value is not None else None,
                "sd": float(r.sd) if r.sd is not None else None,
                "z_score": z,
                "within_2sd": within_2sd,
                "within_3sd": within_3sd,
            })
        return result

    def get_westgard(self, db: Session, analyte: str):
        rows = (
            db.query(QCResult)
            .filter(QCResult.analyte_code == analyte)
            .order_by(QCResult.control_name, QCResult.control_lot, QCResult.run_datetime.asc())
            .all()
        )
        key_fn = lambda r: (r.control_name, r.control_lot)
        groups_out = []
        for key, grp in groupby(rows, key=key_fn):
            grp = list(grp)
            points = []
            for r in grp:
                if r.sd and float(r.sd) > 0 and r.measured_value is not None and r.assigned_value is not None:
                    z = float((r.measured_value - r.assigned_value) / r.sd)
                    points.append((r, z))
                else:
                    points.append((r, None))

            warnings_list = []
            violations_list = []
            for i, (r, z) in enumerate(points):
                if z is None:
                    continue
                if abs(z) > 3:
                    violations_list.append({"rule": "1_3s", "index": i, "run_datetime": str(r.run_datetime), "z_score": round(z, 2)})
                elif abs(z) > 2:
                    warnings_list.append({"rule": "1_2s", "index": i, "run_datetime": str(r.run_datetime), "z_score": round(z, 2)})
                if i >= 1:
                    pz = points[i - 1][1]
                    if pz is not None:
                        if (z > 2 and pz > 2) or (z < -2 and pz < -2):
                            violations_list.append({"rule": "2_2s", "index": i, "run_datetime": str(r.run_datetime), "z_score": round(z, 2)})
                        if abs(z - pz) > 4:
                            violations_list.append({"rule": "R_4s", "index": i, "run_datetime": str(r.run_datetime), "z_score": round(z, 2)})
                if i >= 3:
                    last4 = [points[j][1] for j in range(i - 3, i + 1) if points[j][1] is not None]
                    if len(last4) == 4 and (all(v > 1 for v in last4) or all(v < -1 for v in last4)):
                        violations_list.append({"rule": "4_1s", "index": i, "run_datetime": str(r.run_datetime), "z_score": round(z, 2)})
                if i >= 9:
                    last10 = [points[j][1] for j in range(i - 9, i + 1) if points[j][1] is not None]
                    if len(last10) == 10 and (all(v > 0 for v in last10) or all(v < 0 for v in last10)):
                        violations_list.append({"rule": "10x", "index": i, "run_datetime": str(r.run_datetime), "z_score": round(z, 2)})

            status = "FAIL" if violations_list else ("WARNING" if warnings_list else "PASS")
            groups_out.append({
                "control_name": key[0],
                "control_lot": key[1],
                "n": len(grp),
                "warnings": warnings_list,
                "violations": violations_list,
                "status": status,
            })
        return groups_out

    def export_excel(self, db: Session):
        rows = (
            db.query(QCResult)
            .order_by(QCResult.run_datetime.desc())
            .all()
        )
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "QC Results"
        ws.append([
            "QC ID", "Run DateTime", "Analyte", "Control Name", "Control Lot",
            "Assigned Value", "Measured Value", "SD", "Lower Limit", "Upper Limit",
            "Units", "Reagent Lot",
        ])
        for r in rows:
            ws.append([
                r.qc_id, str(r.run_datetime), r.analyte_code, r.control_name, r.control_lot,
                float(r.assigned_value) if r.assigned_value else None,
                float(r.measured_value) if r.measured_value else None,
                float(r.sd) if r.sd else None,
                float(r.lower_limit) if r.lower_limit else None,
                float(r.upper_limit) if r.upper_limit else None,
                r.units, r.reagent_lot,
            ])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf
