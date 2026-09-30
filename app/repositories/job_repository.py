from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select ,or_ ,func
from app.schemas.job import JobCreate
from app.models.job import Job



class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def getJobByEmployerId(self,user_id:int):
        result = await self.db.execute(select(Job).where(Job.employer_id == user_id))
        return result.scalar_one_or_none()
    


    async def createJob(self,payload:JobCreate,user_id:int):
        job_data = Job(
            title =payload.title,
            description = payload.description,
            company = payload.company,
            location = payload.location,
            job_type = payload.job_type.value
            if hasattr(payload.job_type,"value") 
            else str(payload.job_type),
            experience = payload.experience,
            salary_min = payload.salary_min,
            salary_max = payload.salary_max,
            employer_id = user_id
        )

        self.db.add(job_data)
        await self.db.commit()
        await self.db.refresh(job_data)
        return job_data


    async def getAllJobs(self,
                         offset:int,
                         limit:int,
                         search:str|None=None,
                         job_type:str|None=None,
                         location:str|None=None,
                         is_active:bool|None=None
                         ):
        query = select(Job)

        if search:
            search_value = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Job.title.ilike(search_value),
                    Job.company.ilike(search_value),
                    Job.description.ilike(search_value),
                    Job.location.ilike(search_value)
                )
            )

        if job_type:
            query =query.where(Job.job_type == job_type)    

        if location :
            query = query.where(Job.location.ilike(f"%{location.strip()}%"))

        if is_active is not None :
            query = query.where(Job.is_active == is_active)

        count_query = select(func.count()).select_from(query.subquery()) 
        count_result = await self.db.execute(count_query)

        total = count_result.scalar_one()
        query =(query.order_by(Job.created_at.desc()).offset(offset).limit(limit))

        result = await self.db.execute(query)
        jobs = result.scalars().all()
        return jobs,total


    async def getJobDataById(self,id:int):
        result = await self.db.execute(select(Job).where(Job.id == id))
        return result.scalar_one_or_none()


    async def deletJobId(self,id:int):
        result = await self.db.execute(select(Job).where(Job.id == id)) 
        job =  result.scalar_one_or_none()

        if not job:
            return None 

        await self.db.delete(job)
        await self.db.commit()
        return job


    async def updateJob(self,job:Job):
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job


    async def updateActiveJobs(self,job:Job):
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job

