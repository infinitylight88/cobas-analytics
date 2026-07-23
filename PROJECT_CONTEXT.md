# Cobas Analytics

## Project Overview

Cobas Analytics is a desktop laboratory analytics platform being developed for the **Roche Cobas Integra 400 Plus Clinical Chemistry Analyzer**.

The application imports Cobas monthly archive files, parses every analyzer record, stores normalized data in PostgreSQL, exposes the data through a FastAPI REST API, and will ultimately provide a modern desktop dashboard for laboratory operations, quality control, CAP accreditation, and management reporting.

The application is designed to become the laboratory's analytical layer rather than replacing the existing LIMS.

---

# Primary Goals

The application must answer operational laboratory questions that are difficult or impossible to answer directly from the Cobas analyzer.

Examples include:

* Daily patient workload
* Unique patient samples processed
* Tests performed per patient
* All analytes run on a specific day
* QC performed for each analyte
* Calibration history
* Maintenance history
* Reagent lot history
* ACTG workload
* HbA1c monitoring
* CAP accreditation evidence
* Auditor traceability reports

The system is intended to support laboratory managers, quality officers, auditors, and laboratory technologists.

---

# Technology Stack

## Language

Python 3.13+

---

## Database

PostgreSQL 18

Database name

```
jcrc_chemistry_db
```

---

## ORM

SQLAlchemy ORM

No raw SQL is used inside the API except where absolutely necessary.

---

## API

FastAPI

The API is intentionally separated from the desktop UI so that future applications (desktop, web, reporting tools, mobile) can consume the same backend.

---

## Desktop UI (Planned)

PySide6 (Qt)

The dashboard will consume the FastAPI endpoints rather than querying PostgreSQL directly.

---

# Current Architecture

```
Cobas Archive File
        │
        ▼
 Archive Reader
        │
        ▼
 Record Factory
        │
        ▼
 Record Processors
        │
        ▼
 Database Writers
        │
        ▼
 PostgreSQL
        │
        ▼
 SQLAlchemy ORM
        │
        ▼
 FastAPI
        │
        ▼
 Desktop Dashboard
```

---

# Import Pipeline

Current parser flow

```
Archive File

↓

ArchiveReader

↓

RawWriter

↓

RecordFactory

↓

Processor

↓

PatientWriter
QCWriter
CalibrationWriter
MaintenanceWriter
HostEventWriter

↓

PostgreSQL
```

Every line from the Cobas archive is first stored unchanged inside **raw_records** for complete traceability.

Parsed information is then normalized into dedicated tables.

---

# Database Design

Major tables

```
archive_files
raw_records

patients
patient_results

qc_results

calibrations

maintenance

host_events

parser_log

analytes
analyte_master

control_lots

reagent_lots

instruments
operators
```

The design preserves both:

* original raw archive records
* normalized analytical data

This allows complete audit traceability.

---

# Patient Model

The parser intentionally separates different laboratory workflows.

## LIMS Patients

Normal chemistry samples generally use

```
Accession Number
```

Example

```
1331762-J
```

These are linked to the LIMS.

---

## ACTG Samples

ACTG samples use

```
124xxxx
```

These are research identifiers.

They are intentionally stored separately.

---

## HbA1c

HbA1c is unique because

* patient samples
* controls

share the same assay.

The parser distinguishes them during import.

---

# Current API Structure

```
api/

database/

services/

routers/

schemas/

core/
```

The project follows a Service Layer architecture.

```
Router

↓

Service

↓

ORM

↓

Database
```

Routers contain no business logic.

Services contain all laboratory logic.

---

# Current API Endpoints

## Archive

```
GET /archives
GET /archives/{id}
```

---

## Dashboard

```
GET /dashboard/daily-workload

GET /dashboard/tests-per-patient

GET /dashboard/analytes-per-day

GET /dashboard/department-summary
```

---

## Patients

```
GET /patients/tests/{patient_identifier}
```

---

## QC

```
GET /qc/date/{date}

GET /qc/analyte/{analyte}

GET /qc/summary

GET /qc/compliance

GET /qc/missing
```

Current QC compliance is intentionally simple and will later be refined to accommodate laboratory workflows where QC may be performed after some patient testing.

---

## Calibration

Calibration endpoints implemented.

---

## ACTG

```
GET /actg/{patient_identifier}
```

Returns all tests performed for an ACTG participant.

---

# Development Philosophy

The project is not intended to simply display analyzer data.

Instead it should answer laboratory operational questions.

The API should become an intelligence layer above the analyzer.

Business logic belongs in Services rather than in the UI.

---

# Planned Features

## Dashboard

PySide6 desktop interface including

* Overview
* Daily workload
* QC
* Calibration
* Maintenance
* ACTG
* HbA1c
* Reports

---

## QC Analytics

* Levey-Jennings charts
* Westgard Rules
* QC trends
* Daily QC review
* Missing QC detection
* QC compliance

---

## Calibration Analytics

* Calibration history
* Calibration frequency
* Calibration intervals
* Failed calibrations

---

## ACTG Analytics

* Participant history
* Longitudinal chemistry
* Visit summaries
* Export reports

---

## HbA1c Module

Dedicated module because HbA1c has embedded controls and unique workflows.

---

## CAP Accreditation

The system should answer questions such as

* Was QC run on this date?
* Which controls were used?
* Which reagent lot was active?
* Which calibration preceded patient testing?
* Which patients were affected by a failed QC?
* Which maintenance occurred before testing?
* Show evidence for CAP inspections.

---

## Reporting

Future reporting includes

* PDF reports
* Excel exports
* Monthly summaries
* CAP audit reports
* QC reports
* Calibration reports
* Instrument utilization reports

---

# Coding Standards

* Use SQLAlchemy ORM.
* Keep routers thin.
* Place business logic in Services.
* Maintain database normalization.
* Preserve raw analyzer records for traceability.
* Avoid duplicate logic.
* Write reusable service methods.
* Build API first, then UI.

---

# Current Development Phase

The parser and database are operational.

The REST API is the current focus.

After the API is complete and fully tested, development will move to the PySide6 desktop dashboard, which will consume the API rather than accessing PostgreSQL directly.

The API is intended to remain reusable for future desktop, web, and reporting applications.
