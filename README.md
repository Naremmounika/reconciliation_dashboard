# Reconciliation Engine

A full-stack reconciliation application built using Django REST-style APIs and React.js.

The application compares records from System A and System B and displays discrepancies in a dashboard.

## Features

- Import CSV data for:
  - System A records
  - System B entries
  - Organization and location mappings
- Detect missing records in System B
- Detect orphan records in System B
- Detect duplicate references in System B
- Detect value mismatches
- Filter by organization
- Filter by location
- Filter by discrepancy reason
- Sort by System A or System B value
- Display discrepancy results in a React dashboard
- Automated comparator tests

## Tech Stack

### Backend

- Python
- Django
- SQLite
- django-cors-headers

### Frontend

- React.js
- Vite
- JavaScript
- CSS

## Project Structure

```text
reconciliation-engine/
├── backend/
│   ├── core/
│   ├── reconciler/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── import_data.py
│   │   ├── services/
│   │   │   └── comparator.py
│   │   ├── tests/
│   │   │   └── test_comparator.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
├── data/
│   ├── system_a.csv
│   ├── system_b.csv
│   └── locations.csv
└── README.md

## Setup Instructions
    1. Clone the repository
    git clone <repository-url>
    cd reconciliation-engine
    2. Backend setup
    cd backend
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py import_data
    python manage.py runserver

Backend API:

    http://127.0.0.1:8000/api/discrepancies/

3. Frontend setup
    Open another terminal:

        cd frontend
        npm install
        npm run dev

    Frontend:

        http://localhost:5173/
        API Endpoints
        Get discrepancies
        GET /api/discrepancies/
        Filter by organization
        GET /api/discrepancies/?org_id=ORG-A
        Filter by reason
        GET /api/discrepancies/?reason=VALUE_MISMATCH
        Filter by location
        GET /api/discrepancies/?location_id=LOC-201
        Sort results
        GET /api/discrepancies/?sort=system_a_value
        Get locations
        GET /api/locations/
        Comparator Results

    The imported sample data currently produces:

    7 value mismatches

    3 records missing in System B

    2 duplicate entries in System B

    2 orphan entries in System B

    Total discrepancies: 14.

    Testing

    Run the backend tests:

    cd backend
    python manage.py test reconciler

    The comparator tests cover:

    Missing records

    Orphan records

    Duplicate records

    Value mismatches

Assumptions

    System A record_id is compared with System B record_ref.

    References are normalized by removing non-alphanumeric characters and converting them to lowercase.

    System A total_value is compared with System B value.

    Values are treated as decimal numbers where possible.

    Organization access is currently determined through the location-to-organization mapping.

    Raw CSV values are preserved as text in the database