# Bulk Certificate Generator

A Python backend application that generates PDF certificates in bulk using FastAPI. It validates recipient information, tracks generation jobs, handles individual certificate failures, and provides APIs to retrieve generated certificates.

## Features

- Generate certificates for multiple recipients in one request
- Validate recipient data and email addresses
- Generate PDF certificates using a predefined template
- Store jobs and recipient records in SQLite
- Track job status and success/failure counts
- Handle individual certificate-generation failures independently
- List generation results and download certificates
- Automated API tests using Pytest

## Technology Stack

- **Language:** Python 3.11+
- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **PDF Generation:** ReportLab
- **Testing:** Pytest and FastAPI TestClient

## Project Structure

```text
bulk-certificate-generator/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   └── jobs.py
│   ├── services/
│   │   └── certificate_generator.py
│   └── templates/
├── tests/
│   └── test_jobs.py
├── generated_certificates/
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/HemantSaiTeja/bulk-certificate-generator.git
cd bulk-certificate-generator
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

Start the development server:

```powershell
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

The application uses a local SQLite database and stores generated PDF files locally.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/api/jobs/` | Submit a bulk certificate-generation job |
| GET | `/api/jobs/{job_id}/` | Retrieve job status and counts |
| GET | `/api/jobs/{job_id}/certificates/` | List recipient results |
| GET | `/api/certificates/{certificate_id}/download/` | Download an individual PDF |

## Example Request

Submit a POST request to `/api/jobs/` with the following JSON body:

```json
{
  "recipients": [
    {
      "name": "Rahul Sharma",
      "email": "rahul@example.com",
      "certificate_title": "Python Programming"
    },
    {
      "name": "Priya Reddy",
      "email": "priya@example.com",
      "certificate_title": "Web Development"
    }
  ]
}
```

### Example Response

A successful request returns HTTP `201 Created` with a response similar to:

```json
{
  "job_id": 1,
  "status": "COMPLETED",
  "total_recipients": 2,
  "successful_count": 2,
  "failed_count": 0
}
```

The job ID and counts depend on the submitted request and its results.

Use the returned job ID to retrieve job information and recipient results. Use a successful recipient's certificate ID to download the generated PDF.

## Run Tests

Execute the automated test suite:

```powershell
python -m pytest -v
```

The current test suite covers:

- Home and health endpoints
- Successful job creation
- Invalid email and empty-recipient validation
- Job status retrieval
- Certificate result listing
- PDF downloads
- Individual certificate-generation failures
- Missing-job handling

## Architecture

### Request and Validation Flow

FastAPI receives HTTP requests, and Pydantic validates the incoming recipient data before the generation workflow begins.

### Database Layer

SQLAlchemy manages the SQLite database. A generation job represents a bulk request, while individual recipient records store recipient details, generation status, certificate path, and error information.

### Certificate Generation

The certificate-generation service uses ReportLab to create a PDF for each recipient from a predefined template.

### Failure Handling

Each recipient is processed independently. If generating one certificate fails, the application records that recipient's failure and continues processing the remaining recipients.

### Processing Strategy

The current implementation uses synchronous processing. This keeps the initial architecture simple and easy to run locally, but the client must wait for generation to finish before receiving the final job result.

## Design Decisions

- **FastAPI:** Provides a lightweight framework for building REST APIs and automatic interactive documentation.
- **SQLite:** Avoids requiring a separate database server during local development.
- **SQLAlchemy:** Separates database operations from API logic.
- **ReportLab:** Generates PDF certificates programmatically without requiring an external document-generation service.
- **Per-recipient status tracking:** Allows successful and failed certificate generations to be reported independently.
- **Synchronous processing:** Keeps the initial implementation simple. Background processing would be preferable for larger workloads.

## Learning Outcomes

This project demonstrates practical experience with REST API development, relational database integration, request validation, PDF generation, error handling, automated testing, and Git/GitHub workflows.

## Future Scope

- Background workers and asynchronous job processing
- Pagination for large result sets
- Authentication and authorization
- Multiple certificate templates
- Cloud object storage for generated PDFs
- QR codes or unique verification links
- Docker-based deployment
- Improved test database isolation and dependency management
- Logging, monitoring, and production-ready security controls

## Limitations

This is an initial implementation intended for demonstration and further development. It currently uses synchronous processing and local file storage. Production deployment would require additional security controls, concurrency management, storage management, and operational monitoring.