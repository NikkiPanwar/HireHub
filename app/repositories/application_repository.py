from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func ,or_
from app.schemas.application import ApplicationCreate
from app.models.application import Application


class ApplicationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def getApplicationByUserAndJob(self, user_id: int, job_id: int):
        result = await self.db.execute(
            select(Application).where(
                Application.applicant_id == user_id,
                Application.job_id == job_id
            )
        )
        return result.scalar_one_or_none()
    

    async def getApplicationById(self, application_id: int):
        result = await self.db.execute(select(Application).where(Application.id == application_id))
        return result.scalar_one_or_none()
    

    async def createApplication(self, payload: ApplicationCreate, user_id: int):
        application_data = Application(
            job_id=payload.job_id,
            applicant_id=user_id,
            resume_url=payload.resume_url,
            cover_letter=payload.cover_letter,
            phone_number=payload.phone_number,
            linkedin_url=payload.linkedin_url,
            portfolio_url=payload.portfolio_url,
            years_of_experience=payload.years_of_experience,
            expected_salary=payload.expected_salary
        )
        self.db.add(application_data)
        await self.db.commit()
        await self.db.refresh(application_data)
        return application_data


    async def getApplication(self,
                             offset:int,
                             limit:int,
                             search:str|None=None,
                             application_status:str|None=None
                             ):
        query = select(Application)

        if search :
            search_value = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Application.phone_number.ilike(search_value),
                    Application.linkedin_url.ilike(search_value),
                    Application.portfolio_url.ilike(search_value),
                    Application.cover_letter.ilike(search_value)
                )
            )
        if application_status:
            query = query.where(Application.status == application_status)

        count_query = select(func.count()).select_from(query.subquery())
        count_result=await self.db.execute(count_query)

        total =count_result.scalar_one()
        query = (query.order_by(Application.created_at.desc()).offset(offset).limit(limit))    
    
        result = await self.db.execute(query)
        application = result.scalars().all()
        return application ,total


    async def deleteApplicationById(self,deleteId):
        result = await self.db.execute(select(Application).where(Application.id == deleteId))
        application =  result.scalar_one_or_none()

        if not application :
            return None

        await self.db.delete(application)
        await self.db.commit()
        return application


    async def updateApplication(self,application:Application):
        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)
        return application


    async def updateApplicationStatus(self,application:Application):
        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)
        return application


    async def getMyApplication(self,
                               applicant_id:int,
                               offset:int,
                               limit:int,
                               search:str|None=None,
                               status:str|None=None
                               ):
        query = select(Application).where(Application.applicant_id == applicant_id)

        if search :
            search_value = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Application.cover_letter.ilike(search_value),
                    Application.portfolio_url.ilike(search_value),
                    Application.status.ilike(search_value)
                )
            )

        if status :
            query = query.where(Application.status == status)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.db.execute(count_query) 

        total = count_result.scalar_one()
        query = (query.order_by(Application.created_at.desc()).offset(offset).limit(limit))

        result = await self.db.execute(query)
        application = result.scalars().all()
        return application, total


    