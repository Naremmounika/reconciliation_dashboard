# Technical Decisions

## 1. Backend Framework

Django was selected for the backend because it provides a clear project structure, database integration, routing, and testing support.

## 2. Frontend Framework

React.js with Vite was selected for the frontend because it supports a simple and responsive dashboard implementation.

## 3. Database

SQLite was selected because the assignment is time-boxed and the sample data is small.

## 4. CSV Import

A Django management command was created to import:

- `system_a.csv`
- `system_b.csv`
- `locations.csv`

The importer uses `update_or_create` so that data can be imported repeatedly without creating unnecessary duplicate database records.

## 5. Reference Normalization

System B references are normalized by:

- Converting text to lowercase
- Removing non-alphanumeric characters

This allows values such as `A-1001` and `a1001` to be compared as the same reference.

## 6. Discrepancy Detection

The comparator detects:

- Records missing in System B
- Orphan records in System B
- Duplicate System B entries
- Value mismatches

The comparison logic is kept separately in:

```text
backend/reconciler/services/comparator.py

7. Tenant and Location Filtering

Organization access is derived from the organization-to-location mapping in locations.csv.

The current implementation filters records using the org_id query parameter.

Authentication and role-based authorization were not implemented because they were outside the limited assignment scope. Therefore, this implementation should be considered a functional demonstration of tenant filtering rather than a production-ready security boundary.

8. Data Preservation

CSV values are stored as text to preserve the original values, including dirty or inconsistent data.

Values are converted to decimal numbers only during comparison when possible.

9. API Design

The backend exposes simple GET endpoints:

/api/discrepancies/

/api/locations/

Filtering and sorting are handled through query parameters.

10. Testing

The comparator has automated tests covering:

Missing records

Orphan records

Duplicate records

Value mismatches