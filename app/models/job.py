from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)
    job_type = Column(String(50), nullable=True, default="full_time")  # full_time, part_time, remote, contract, internship
    experience = Column(Integer, nullable=True)  # years of experience required
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    employer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow().replace(tzinfo=None), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.utcnow().replace(tzinfo=None), onupdate=lambda: datetime.utcnow().replace(tzinfo=None), nullable=False)

    # Relationships
    employer = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
