from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    applicant_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resume_url = Column(String(500), nullable=True)
    cover_letter = Column(Text, nullable=True)
    phone_number = Column(String(20), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    portfolio_url = Column(String(255), nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    expected_salary = Column(Integer, nullable=True)
    status = Column(String(50), default="APPLIED", nullable=False)  # APPLIED, SHORTLISTED, INTERVIEW, REJECTED, HIRED, WITHDRAWN
    created_at = Column(DateTime, default=lambda: datetime.utcnow().replace(tzinfo=None), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.utcnow().replace(tzinfo=None), onupdate=lambda: datetime.utcnow().replace(tzinfo=None), nullable=False)

    # Relationships
    job = relationship("Job", back_populates="applications")
    applicant = relationship("User", back_populates="applications")
