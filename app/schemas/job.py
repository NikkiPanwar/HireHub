from datetime import datetime
from enum import Enum
from typing import Optional ,List
from pydantic import BaseModel, ConfigDict


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    REMOTE = "remote"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class JobBase(BaseModel):
    title: str
    description: str
    company: str
    location: str
    job_type: JobType = JobType.FULL_TIME
    experience: Optional[int] = None  
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    experience: Optional[int] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    is_active: Optional[bool] = None


class JobStatusUpdate(BaseModel):
    is_active: bool  # True = Open, False = Closed


class JobResponse(JobBase):
    id: int
    is_active: bool
    employer_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobCreateResponse(BaseModel):
    data: JobResponse
    message: str
    success: bool

class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int       

class AllJobResponse(BaseModel):
    data: List[JobResponse]
    pagination:PaginationResponse
    message: str
    success: bool


class UpdateJobResponse(BaseModel):
    data: JobResponse
    message: str
    success: bool