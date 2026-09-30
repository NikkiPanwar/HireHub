from typing import Dict 
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.exceptions.custom_exception import CustomException
from app.config.database import get_db
from app.repositories.job_repository import JobRepository
from app.repositories.user_repository import UserRepository
import math
from app.schemas.job import JobUpdate,JobCreate,JobStatusUpdate

import logging 

logger = logging.getLogger(__name__)


class JobService:

    def __init__(self,db:AsyncSession =Depends(get_db)):
        self.jobRepo = JobRepository(db)
        self.UserRepo = UserRepository(db)


    async def createJob(
            self,
            payload:JobCreate,
            user_id:int
            )->Dict :

        try :

            if (
                not payload.title 
                or not payload.description 
                or not payload.company 
                or not payload.location 
                or not payload.job_type
            ):
                raise CustomException("these are required fields")

            checkUser = await self.UserRepo.getUsersById(user_id)

            if not checkUser:
                raise CustomException("User not found", status_code=404)
            
            create_data = await self.jobRepo.createJob(payload,user_id)

            return create_data

        except CustomException :
            raise 

        except Exception as e :
            logger.error(f"system error:{str(e)}",exc_info=True)

            raise CustomException("unexcepted error occur",status_code=500)


    async def getAllJobs(self,
                         page:int,
                         limit:int,
                         search:str| None = None,
                         job_type:str | None = None,
                         location:str | None = None,
                         is_active:bool|None = None
                         )->Dict:
        try :
            offset = (page-1)*limit

            getData ,total = await self.jobRepo.getAllJobs(
                offset=offset,
                limit=limit,
                search = search ,
                job_type= job_type ,
                location = location,
                is_active = is_active
            )

            total_pages = math.ceil(total/limit)

            if total == 0 :
                raise CustomException("no jobs found",status_code=404)

            if page > total_pages:
                raise CustomException(f"Page {page} does not exist.Total pages:{total_pages}",status_code=404)


            return {
                "data": getData ,
                "pagination":{
                    "page":page,
                    "limit":limit,
                    "total":total,
                    "total_pages":total_pages
                }
            }    

        except CustomException:
            raise 

        except Exception as e :
            logger.error(f"job fetching erros:{str(e)}",exc_info=True)
            raise CustomException("unexcepted error occur",status_code=500)
        

    async def getAllJobsById(self,id:int):
            try :
    
                getJobDataById = await self.jobRepo.getJobDataById(id)

                if not getJobDataById:
                 raise CustomException("data not found",status_code=400)

                return getJobDataById
            
            except CustomException:
                raise 
    
            except Exception as e :
                logger.error(f"job fetching erros:{str(e)}",exc_info=True)
                raise CustomException("unexcepted error occur",status_code=500)
            

    async def deletJobId(self,id:int):
        try :
            jobId = await self.jobRepo.deletJobId(id)

            if not jobId:
                raise CustomException("job id not found",status_code=404)
            return None

        except CustomException :
            raise 

        except Exception as e :
            logger.error(f"job delete error:{str(e)}",exc_info=True)
            raise CustomException("unexcepted error occure",status_code=500)


    async def updateJob(self,id:int,payload:JobUpdate):
        try :
            if not id :
                raise CustomException("id not found",status_code=400)

            existData = await self.jobRepo.getJobDataById(id)

            if not existData :
                raise CustomException("user data not found",status_code=404)

            if (
             payload.location is None 
             and payload.job_type is None
             and payload.salary_max is None 
             and payload.description is None
             and payload.salary_min is None
             and payload.company is None
             and payload.title is  None ):

             raise CustomException("atleast one field is required to update the job",status_code=400)

            if payload.title is not None:
                existData.title = payload.title

            if payload.description is not None :
                existData.description  = payload.description 

            if payload.company is not None :
                existData.company = payload.company

            if payload.location is not None :    
                existData.location = payload.location 

            if payload.job_type is not None :
                existData.job_type = payload.job_type

            if payload.experience is not None :
                existData.experience = payload.experience

            if payload.salary_min is not None :
                existData.salary_min = payload.salary_min

            if payload.salary_max is not None :
                existData.salary_max = payload.salary_max

            return await self.jobRepo.updateJob(existData)    

        except IntegrityError :
            await self.jobRepo.db.rollback()
            raise CustomException("title already exists",status_code=400)

        except CustomException as e :
            logger.error(f"system error:{str(e)}",exc_info=True)
            raise 


    async def updatedActiveData(self,id:int,payload:JobStatusUpdate)->Dict:
        try :
            if not id:
                raise CustomException("id not found",status_code=400)
            
            existingData = await self.jobRepo.getJobDataById(id)

            if not existingData :
                raise CustomException("job data not found",status_code=404)

            existingData.is_active = payload.is_active

            return await self.jobRepo.updateActiveJobs(existingData)

        except CustomException:
            raise 

        except Exception as e :
            logger.error(f"job status active change error:{str(e)}",exc_info=True)
            raise CustomException("unexcepted error occur",status_code=500)
        

        



