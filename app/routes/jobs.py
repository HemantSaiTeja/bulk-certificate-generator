
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GenerationJob, Recipient
from app.schemas import GenerationRequest
from app.services.certificate_generator import generate_certificate


router = APIRouter(prefix="/api", tags=["Certificate Jobs"])


@router.post("/jobs/", status_code=201)
def create_job(
    request: GenerationRequest,
    db: Session = Depends(get_db),
):
    job = GenerationJob(
        status="PROCESSING",
        total_recipients=len(request.recipients),
        successful_count=0,
        failed_count=0,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for item in request.recipients:
        recipient = Recipient(
            job_id=job.id,
            name=item.name.strip(),
            email=str(item.email),
            certificate_title=item.certificate_title.strip(),
            status="PENDING",
        )
        db.add(recipient)

    db.commit()

    recipients = (
        db.query(Recipient)
        .filter(Recipient.job_id == job.id)
        .all()
    )

    for recipient in recipients:
        try:
            recipient.status = "PROCESSING"
            db.commit()

            path = generate_certificate(
                recipient.id,
                recipient.name,
                recipient.certificate_title,
            )

            recipient.certificate_path = path
            recipient.status = "SUCCESS"
            recipient.error_message = None

        except Exception as exc:
            recipient.status = "FAILED"
            recipient.error_message = (
                f"Certificate generation failed: {str(exc)[:300]}"
            )

        db.commit()

    job.successful_count = (
        db.query(Recipient)
        .filter(
            Recipient.job_id == job.id,
            Recipient.status == "SUCCESS",
        )
        .count()
    )

    job.failed_count = (
        db.query(Recipient)
        .filter(
            Recipient.job_id == job.id,
            Recipient.status == "FAILED",
        )
        .count()
    )

    if job.failed_count:
        job.status = "COMPLETED_WITH_ERRORS"
    else:
        job.status = "COMPLETED"

    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "status": job.status,
        "total_recipients": job.total_recipients,
        "successful_count": job.successful_count,
        "failed_count": job.failed_count,
    }


@router.get("/jobs/{job_id}/")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "status": job.status,
        "total_recipients": job.total_recipients,
        "successful_count": job.successful_count,
        "failed_count": job.failed_count,
        "created_at": job.created_at,
    }


@router.get("/jobs/{job_id}/certificates/")
def list_certificates(job_id: int, db: Session = Depends(get_db)):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    recipients = db.query(Recipient).filter(
        Recipient.job_id == job_id
    ).all()

    return [
        {
            "certificate_id": recipient.id,
            "name": recipient.name,
            "email": recipient.email,
            "status": recipient.status,
            "error_message": recipient.error_message,
            "download_url": (
                f"/api/certificates/{recipient.id}/download/"
                if recipient.status == "SUCCESS"
                else None
            ),
        }
        for recipient in recipients
    ]


@router.get("/certificates/{certificate_id}/download/")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    recipient = db.query(Recipient).filter(
        Recipient.id == certificate_id
    ).first()

    if recipient is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found",
        )

    if recipient.status != "SUCCESS" or not recipient.certificate_path:
        raise HTTPException(
            status_code=409,
            detail="Certificate is not available",
        )

    path = Path(recipient.certificate_path)

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found",
        )

    return FileResponse(
        path=str(path),
        media_type="application/pdf",
        filename=f"certificate_{recipient.id}.pdf",
    )
