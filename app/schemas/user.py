from datetime import datetime
from enum import Enum
from typing import Optional ,List
from pydantic import BaseModel, ConfigDict


class UserRole(str, Enum):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"
    ADMIN = "admin"


class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.CANDIDATE


class UserCreate(UserBase):
    password: str


class UserAdminCreate(UserBase):
    password: str
    is_active: bool = True


class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserStatusUpdate(BaseModel):
    is_active: bool


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthRegisterResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    message: str = "User registered successfully"

class UserListResponse(BaseModel):
    data: List[UserResponse]
    message: str = "User details fetched successfully"


# ---------------------------------------------------------------------------
# Authentication Schemas
# ---------------------------------------------------------------------------

class UserLogin(BaseModel):
    username_or_email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    message:Optional[str]=None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    email:str


class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserDetailResponse(BaseModel):
    data: UserResponse
    message: str

class ForgotPasswordResponse(BaseModel):
    email: str
    message: str


class UpdateUser(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    user_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    job_type: str
    experience: int | None = None

    model_config = ConfigDict(from_attributes=True)


class UserProfileResponse(UserResponse):
    jobs: list[JobResponse] = []

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(BaseModel):
    data: UserProfileResponse
    message: str        

class UserAccountActiveRequest(BaseModel):
    is_active:bool

    
