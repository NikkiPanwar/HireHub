from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.job import PaginationResponse


class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEW = "INTERVIEW"
    REJECTED = "REJECTED"
    HIRED = "HIRED"
    WITHDRAWN = "WITHDRAWN"


class ApplicationBase(BaseModel):
    job_id: int
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    years_of_experience: Optional[int] = None
    expected_salary: Optional[int] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    years_of_experience: Optional[int] = None
    expected_salary: Optional[int] = None


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(ApplicationBase):
    id: int
    applicant_id: int
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationCreateResponse(BaseModel):
    data: ApplicationResponse
    message: str
    success: bool = True


class AllApplicationResponse(BaseModel):
    data: List[ApplicationResponse]
    pagination: Optional[PaginationResponse] = None
    message: str
    success: bool = True


class UpdateApplicationResponse(BaseModel):
    data: ApplicationResponse
    message: str
    success: bool = True


class ApplicationStatusResponse(BaseModel):
    data: ApplicationResponse
    message: str
    success: bool = True


class MyApplicationsResponse(BaseModel):
    data: List[ApplicationResponse]
    pagination: Optional[PaginationResponse] = None
    message: str
    success: bool = True


class JobApplicationsResponse(BaseModel):
    data: List[ApplicationResponse]
    pagination: Optional[PaginationResponse] = None
    message: str
    success: bool = True


class UserApplicationsResponse(BaseModel):
    data: List[ApplicationResponse]
    pagination: Optional[PaginationResponse] = None
    message: str
    success: bool = True


class ApplicationResponseWrapper(BaseModel):
    data: ApplicationResponse
    message: str
    success: bool = True    


class DeleteResponseWrapper(BaseModel):
    data: None
    message: str
    success: bool = True    



class MyApplicationResponse(BaseModel):
    id: int
    job_id: int
    applicant_id: int
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    years_of_experience: Optional[int] = None
    expected_salary: Optional[int] = None
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MyApplicationsResponseWrapper(BaseModel):
    data: List[MyApplicationResponse]
    pagination: Optional[PaginationResponse] = None
    message: str
    success: bool = True


class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
