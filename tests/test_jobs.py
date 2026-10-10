
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine

client = TestClient(app)


def create_payload():
    return {
        "recipients": [
            {
                "name": "Test User",
                "email": "test@example.com",
                "certificate_title": "Python Programming",
            }
        ]
    }


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_job():
    response = client.post("/api/jobs/", json=create_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["total_recipients"] == 1
    assert data["successful_count"] == 1
    assert data["failed_count"] == 0


def test_invalid_email():
    payload = create_payload()
    payload["recipients"][0]["email"] = "invalid-email"

    response = client.post("/api/jobs/", json=payload)

    assert response.status_code == 422


def test_empty_recipients():
    response = client.post(
        "/api/jobs/",
        json={"recipients": []},
    )

    assert response.status_code == 422


def test_get_job_status():
    created = client.post(
        "/api/jobs/",
        json=create_payload(),
    )
    job_id = created.json()["job_id"]

    response = client.get(f"/api/jobs/{job_id}/")

    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"


def test_list_certificates():
    created = client.post(
        "/api/jobs/",
        json=create_payload(),
    )
    job_id = created.json()["job_id"]

    response = client.get(
        f"/api/jobs/{job_id}/certificates/"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "SUCCESS"


def test_download_certificate():
    created = client.post(
        "/api/jobs/",
        json=create_payload(),
    )
    job_id = created.json()["job_id"]

    certificates = client.get(
        f"/api/jobs/{job_id}/certificates/"
    ).json()

    certificate_id = certificates[0]["certificate_id"]

    response = client.get(
        f"/api/certificates/{certificate_id}/download/"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_individual_generation_failure():
    payload = {
        "recipients": [
            {
                "name": "Successful User",
                "email": "success@example.com",
                "certificate_title": "Python",
            },
            {
                "name": "Failed User",
                "email": "failure@example.com",
                "certificate_title": "Java",
            },
        ]
    }

    original_generator = (
        "app.routes.jobs.generate_certificate"
    )

    def generate_with_one_failure(recipient_id, name, title):
        if name == "Failed User":
            raise RuntimeError("Simulated PDF failure")

        from app.services.certificate_generator import (
            generate_certificate,
        )

        return generate_certificate(
            recipient_id, name, title
        )

    with patch(
        original_generator,
        side_effect=generate_with_one_failure,
    ):
        response = client.post(
            "/api/jobs/",
            json=payload,
        )

    assert response.status_code == 201

    data = response.json()
    assert data["status"] == "COMPLETED_WITH_ERRORS"
    assert data["successful_count"] == 1
    assert data["failed_count"] == 1

    certificates = client.get(
        f"/api/jobs/{data['job_id']}/certificates/"
    ).json()

    statuses = {item["name"]: item["status"] for item in certificates}

    assert statuses["Successful User"] == "SUCCESS"
    assert statuses["Failed User"] == "FAILED"


def test_missing_job():
    response = client.get("/api/jobs/999999999/")

    assert response.status_code == 404
