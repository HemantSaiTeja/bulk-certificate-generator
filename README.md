
# Bulk Certificate Generator

A Python backend application for generating PDF certificates in bulk using FastAPI.

## Features

- Bulk certificate generation
- Recipient input validation
- PDF certificate generation
- SQLite database with SQLAlchemy
- Job status tracking
- Individual success and failure handling
- Certificate listing and download APIs
- Automated tests with Pytest

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- ReportLab
- Pytest

## Setup

Create a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

```powershell
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to access the interactive API documentation.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/api/jobs/` | Create a bulk generation job |
| GET | `/api/jobs/{job_id}/` | Get job status |
| GET | `/api/jobs/{job_id}/certificates/` | List certificate results |
| GET | `/api/certificates/{certificate_id}/download/` | Download a certificate |

## Run Tests

```powershell
python -m pytest -v
```

The tests cover API responses, input validation, job status, certificate generation, individual failures, and downloads.

## Architecture

FastAPI handles HTTP requests. Pydantic validates recipient data. SQLAlchemy stores jobs and recipient records in SQLite. ReportLab generates PDF certificates using a predefined template.

The current implementation processes requests synchronously and stores generated files locally.

## Learning Outcomes

- REST API development
- Database integration
- Data validation
- PDF generation
- Error handling
- Automated testing
- Git and GitHub workflows

## Future Scope

- Background task processing
- Authentication and authorization
- Multiple certificate templates
- Cloud file storage
- Certificate verification using QR codes
- Docker deployment
- Improved test database isolation

## Limitations

The current version uses synchronous processing and local storage. Additional security, concurrency controls, and monitoring would be needed for production deployment.
    