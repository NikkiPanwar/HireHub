from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.user import (
    UserRole,
    UserBase,
    UserCreate,
    UserAdminCreate,
    UserUpdate,
    UserStatusUpdate,
    UserResponse,
    UserLogin,
    Token,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
    TokenPayload,
)
from app.schemas.job import (
    JobType,
    JobBase,
    JobCreate,
    JobUpdate,
    JobStatusUpdate,
    JobResponse,
)
from app.schemas.application import (
    ApplicationStatus,
    ApplicationBase,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationStatusUpdate,
    ApplicationResponse,
    ApplicationCreateResponse,
    AllApplicationResponse,
    UpdateApplicationResponse,
)

__all__ = [
    # Common
    "MessageResponse",
    "PaginatedResponse",
    # User / Auth
    "UserRole",
    "UserBase",
    "UserCreate",
    "UserAdminCreate",
    "UserUpdate",
    "UserStatusUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "RefreshTokenRequest",
    "ForgotPasswordRequest",
    "ResetPasswordRequest",
    "ChangePasswordRequest",
    "TokenPayload",
    # Job
    "JobType",
    "JobBase",
    "JobCreate",
    "JobUpdate",
    "JobStatusUpdate",
    "JobResponse",
    # Application
    "ApplicationStatus",
    "ApplicationBase",
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationStatusUpdate",
    "ApplicationResponse",
    "ApplicationCreateResponse",
    "AllApplicationResponse",
    "UpdateApplicationResponse",
]
