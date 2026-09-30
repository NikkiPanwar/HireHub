# Job Management API

A production-ready, modular REST API for job postings and applications built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **JWT Authentication**.

---

## 🏛 Architecture Pattern

The application implements a clean, layered **Router → Service → Repository** architectural pattern:

```
Request  ──►  Router (app/routers/)
                │  • Validates input schema
                │  • Handles HTTP status & responses
                ▼
              Service (app/services/)
                │  • Implements business logic
                │  • Enforces permissions & domain rules
                ▼
              Repository (app/repositories/)
                │  • Encapsulates database queries (SQLAlchemy)
                │  • Isolates ORM details
                ▼
              Database (PostgreSQL)
```

---

## 📁 Project Structure

```
job-management-api/
│
├── app/
│   ├── main.py                     # FastAPI application factory & router registration
│   │
│   ├── core/                       # Core configuration & infrastructure
│   │   ├── config.py               # Pydantic Settings & environment variables
│   │   ├── database.py             # Database engine, SessionLocal & get_db dependency
│   │   └── security.py             # Password hashing (bcrypt) & JWT token utilities
│   │
│   ├── models/                     # SQLAlchemy ORM database models
│   │   ├── user.py                 # User model (applicant / employer / admin)
│   │   ├── job.py                  # Job listing model
│   │   └── application.py          # Job application model
│   │
│   ├── schemas/                    # Pydantic request/response validation schemas
│   │   ├── user.py                 # User and Token schemas
│   │   ├── job.py                  # Job schemas
│   │   └── application.py          # Application schemas
│   │
│   ├── routers/                    # FastAPI route handlers / controllers
│   │   ├── auth.py                 # /api/v1/auth (register, login)
│   │   ├── users.py                # /api/v1/users (profile, update)
│   │   ├── jobs.py                 # /api/v1/jobs (CRUD, search, filter)
│   │   └── applications.py         # /api/v1/applications (apply, view, review)
│   │
│   ├── services/                   # Business logic layer
│   │   ├── auth_service.py         # Registration & authentication logic
│   │   ├── user_service.py         # User operations
│   │   ├── job_service.py          # Job management & permission checks
│   │   └── application_service.py  # Application flow & duplicate checks
│   │
│   └── repositories/               # Data access layer
│       ├── user_repository.py      # User DB queries
│       ├── job_repository.py       # Job DB queries & search filters
│       └── application_repository.py# Application DB queries
│
├── alembic/                        # Alembic database migration scripts
│   ├── versions/                   # Generated migration revisions
│   ├── env.py                      # Alembic migration environment
│   └── script.py.mako              # Revision file template
│
├── alembic.ini                     # Alembic configuration
├── .env                            # Environment variables (do NOT commit)
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- PostgreSQL server running locally or via Docker

### 2. Configure Environment (`.env`)
Create or edit your `.env` file in the project root:

```env
PROJECT_NAME="Job Management API"
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/YOUR_DB_NAME
SECRET_KEY="replace-with-a-secure-random-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Run Database Migrations
Generate initial migration and apply it:

```powershell
# Create initial migration from models
alembic revision --autogenerate -m "Initial tables"

# Apply migrations to database
alembic upgrade head
```

### 4. Run the Application
Start the Uvicorn development server:

```powershell
uvicorn app.main:app --reload
```

---

## 📖 API Documentation

Once the server is running, explore the interactive documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔑 Key Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new user | No |
| `POST` | `/api/v1/auth/login` | Login with credentials for JWT | No |
| `GET` | `/api/v1/users/me` | Get current user profile | Yes |
| `GET` | `/api/v1/jobs/` | List jobs with filter & search | No |
| `POST` | `/api/v1/jobs/` | Create job posting | Employer / Admin |
| `GET` | `/api/v1/jobs/{id}` | Get job details | No |
| `POST` | `/api/v1/applications/` | Apply for a job | Applicant |
| `GET` | `/api/v1/applications/my` | View my submitted applications | Yes |
| `GET` | `/api/v1/applications/job/{id}` | View applications for a job | Employer (Owner) |
