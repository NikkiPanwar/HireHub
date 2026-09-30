from fastapi import FastAPI
from app.core.database import Base, engine
from app import models
from app.routers import auth ,users ,jobs ,applications


app = FastAPI()

from sqlalchemy import text

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(applications.router)


@app.get("/")
def read_root():
    return {"message": "API is running"}

