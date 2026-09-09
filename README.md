# CareSync Patient Portal

A hospital patient portal built during the CareSync 22-day program.

## Project Overview

CareSync is a hospital patient portal that provides patient, doctor, appointment, and billing data through a FastAPI backend and a web dashboard.

The project includes:
- Patient management
- Doctor information
- Appointment data
- Billing information
- Hospital summary analytics
- Revenue trend analytics
- Appointment heatmap
- Blood group distribution
- Doctor appointment analytics
- Patient search by Patient ID

## Technology Stack

- Python
- FastAPI
- MySQL
- MySQL Connector/Python
- HTML
- CSS
- JavaScript
- Chart.js
- Vue.js

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/summary` | Get hospital summary statistics |
| GET | `/patients` | Get patient data |
| GET | `/patients/{patient_id}` | Get a patient by ID |
| GET | `/patients/{patient_id}/appointments` | Get appointments for a patient |
| GET | `/billing` | Get billing data |
| GET | `/doctors` | Get doctor data |
| GET | `/analytics/doctors` | Get doctor appointment analytics |

## How to Run

### 1. Start the FastAPI backend

Open Command Prompt or PowerShell from the project root:

```text
cd C:\DevLead\caresync-patient-portal
python -m uvicorn dashboard.main:app --reload --port 8000