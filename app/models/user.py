from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="candidate", nullable=False)  # "candidate", "recruiter", "admin"
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow().replace(tzinfo=None), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.utcnow().replace(tzinfo=None), onupdate=lambda: datetime.utcnow().replace(tzinfo=None), nullable=False)

    # Relationships
    jobs = relationship("Job", back_populates="employer", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="applicant", cascade="all, delete-orphan")
