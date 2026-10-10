
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(20), default="PENDING", nullable=False)
    total_recipients = Column(Integer, default=0, nullable=False)
    successful_count = Column(Integer, default=0, nullable=False)
    failed_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    recipients = relationship(
        "Recipient",
        back_populates="job",
        cascade="all, delete-orphan",
    )


class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(
        Integer,
        ForeignKey("generation_jobs.id"),
        nullable=False,
    )
    name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    certificate_title = Column(String(200), nullable=False)
    status = Column(String(20), default="PENDING", nullable=False)
    certificate_path = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)

    job = relationship("GenerationJob", back_populates="recipients")
