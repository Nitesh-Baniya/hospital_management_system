# Hospital Management System

A Flask + MySQL web application for basic hospital operations management.

## Overview

This project provides a simple interface to manage:

- Patients
- Doctors
- Appointments
- Billing
- Reports
- Rooms
- A dashboard view with combined data

The backend is built with Flask and uses MySQL as the data store.

## Tech Stack

- Python 3
- Flask
- MySQL
- Jinja2 templates

## Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Database Setup

The app expects a MySQL database with this configuration in `app.py`:

- Host: `localhost`
- User: `root`
- Password: empty string (`""`)
- Database: `hospital_db`

Use the included schema reference file:

- `hospital_db_schema.pdf`

An ERD diagram is also available:

- `ERD.jpg`

### Important

Update the database credentials in `get_db()` inside `app.py` if your local MySQL setup is different.

## Run the App

From the project root:

```bash
python app.py
```

Then open:

- <http://127.0.0.1:5000/>

The root route redirects to `/dashboard`.

## Available Routes (High Level)

- `/dashboard`
- `/patients`, `/add_patient`, `/edit_patient/<id>`, `/delete_patient/<id>`
- `/doctors`
- `/appointments`, `/add_appointment`, `/delete_appointment/<id>`
- `/bills`, `/add_bill`, `/mark_bill_paid/<id>`, `/delete_bill/<id>`
- `/reports`, `/add_report`, `/view_report/<id>`, `/delete_report/<id>`
- `/rooms`, `/add_room`, `/toggle_room_status/<id>`, `/delete_room/<id>`

## Project Structure

```text
hospital_management_system/
|-- app.py
|-- requirements.txt
|-- hospital_db_schema.pdf
|-- ERD.jpg
`-- templates/
    |-- doctors.html
    |-- edit_patient.html
    |-- patients.html
    |-- reports.html
    |-- rooms.html
    `-- view_report.html
```

## Notes and Current Limitations

- `app.py` references `dashboard.html`, `appointments.html`, and `bills.html`, but these templates are not present in the current `templates/` folder. Accessing those routes will raise template errors unless these files are added.
- The `/edit_patient/<patient_id>` route contains POST handling logic, but the route declaration currently does not include `methods=['GET', 'POST']`.

## Suggested Next Improvements

- Add missing templates for dashboard, appointments, and bills.
- Add proper error handling for database failures.
- Move DB credentials to environment variables.
- Add input validation and server-side form validation.
- Add automated tests for key routes and database operations.
