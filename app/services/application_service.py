from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.custom_exception import CustomException
from app.config.database import get_db
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_repository import JobRepository
from app.repositories.user_repository import UserRepository
from app.schemas.application import ApplicationCreate,ApplicationUpdate
from sqlalchemy.exc import IntegrityError
import math


import logging 

logger = logging.getLogger(__name__)


class ApplicationService:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.applicationRepo = ApplicationRepository(db)
        self.jobRepo = JobRepository(db)
        self.userRepo = UserRepository(db)

    async def createApplication(self, payload: ApplicationCreate, user_id: int):
        try:
            if not payload.job_id:
                raise CustomException("job_id is required", status_code=400)

            job = await self.jobRepo.getJobDataById(payload.job_id)
            if not job:
                raise CustomException("Job not found", status_code=404)

            if not job.is_active:
                raise CustomException("This job is no longer accepting applications", status_code=400)

            if job.employer_id == user_id:
                raise CustomException("You cannot apply to your own job", status_code=400)

            existing_application = await self.applicationRepo.getApplicationByUserAndJob(user_id, payload.job_id)
            if existing_application:
                raise CustomException("You have already applied for this job", status_code=400)

            create_application = await self.applicationRepo.createApplication(payload, user_id)
            return create_application

        except CustomException:
            raise

        except Exception as e:
            logger.error(f"Application creation error: {str(e)}", exc_info=True)
            raise CustomException("Unexpected error occurred", status_code=500)


    async def getApplications(self,
                              page:int,
                              limit:int,
                              search:str|None=None,
                              application_status:str|None=None
                              ):
        try :
            offset = (page-1)*limit
            getApplicationData , total = await self.applicationRepo.getApplication(
               offset=offset,
               limit=limit,
               search=search,
               application_status=application_status
            )

            total_pages = math.ceil(total/limit )

            if total == 0:
                 raise CustomException("no applications found",status_code=404)

            if page > total_pages:
                 raise CustomException(f"page{page} does not exist.Total pages:{total_pages}",status_code=404)
            
            if not getApplicationData :
                raise CustomException("data not found",status_code=400)

            return {
                "data":getApplicationData,
                "pagination":{
                    "page":page,
                    "limit":limit,
                    "total":total,
                    "total_pages":total_pages
                }
          }

        except CustomException:
                    raise
        
        except Exception as e:
            logger.error(f"Application get data error: {str(e)}", exc_info=True)
            raise CustomException("Unexpected error occurred", status_code=500)
        

    async def getApplicationById(self,application_id:int):
        try :
              getApplicationById = await self.applicationRepo.getApplicationById(application_id)

              if not application_id :
                   raise CustomException("application_id not found",status_code=400)
                   
              if not getApplicationById :
                   raise CustomException("data not found",status_code=400)
              return getApplicationById

        except CustomException :
             raise 

        except Exception as e:
             logger.error(f"application by id error:{str(e)}",exc_info=True)
             raise CustomException("unexcepted error occured",status_code=500)


    async def deleteApplicationById(self,deleteId:int):
        try :
            await self.applicationRepo.deleteApplicationById(deleteId)

            if not deleteId :
                   raise CustomException("deleteId not found",status_code=400)

        except CustomException :
             raise 

        except Exception as e:
             logger.error(f"application by id error:{str(e)}",exc_info=True)
             raise CustomException("unexcepted error occured",status_code=500)


    async def updateApplicationById(self,updateId:int,payload:ApplicationUpdate):
         try :
               if not updateId:
                    raise CustomException("update id not found",status_code=400)
               
               checkExistData = await self.applicationRepo.getApplicationById(updateId)

               if  not checkExistData :
                    raise CustomException("applications data not found",status_code=400)

               if(
                    payload.cover_letter is None and
                    payload.expected_salary is None and
                    payload.linkedin_url is None and 
                    payload.phone_number is None and 
                    payload.portfolio_url is None and
                    payload.years_of_experience is None 
               ):
                    raise CustomException("atleast one field is required to update",status_code=400)
              
               if payload.years_of_experience is not None:
                    checkExistData.years_of_experience = payload.years_of_experience

               if payload.cover_letter is not None :
                    checkExistData.cover_letter = payload.cover_letter

               if payload.expected_salary is not None :
                    checkExistData.expected_salary = payload.expected_salary

               if payload.linkedin_url is not None :
                    checkExistData.linkedin_url = payload.linkedin_url

               if payload.phone_number is not None :
                    checkExistData.phone_number = payload.phone_number 

               if payload.portfolio_url is not None :
                    checkExistData.portfolio_url = payload.portfolio_url

               return await self.applicationRepo.updateApplication(checkExistData)
         
         except IntegrityError:
                await self.applicationRepo.db.rollback()
                raise CustomException("phone num",status_code=400)
         
         except CustomException as e :
              logger.error(f"system error:{str(e)}",exc_info=True)
              raise


    async def updateApplicationStatus(self,updateId:int,status:str):
         try :
               if not updateId:
                    raise CustomException("update id not found",status_code=400)
               
               checkExistData = await self.applicationRepo.getApplicationById(updateId)

               if  not checkExistData :
                    raise CustomException("applications data not found",status_code=400)

               if not status:
                    raise CustomException("status is required to update",status_code=400)
              
               checkExistData.status = status

               return await self.applicationRepo.updateApplicationStatus(checkExistData)
         
         except CustomException:
                raise
         
         except CustomException as e :
              logger.error(f"system error:{str(e)}",exc_info=True)
              raise CustomException("Failed to update application status", status_code=500)


    async def getMyApplication(self,
                           user_id:int,    
                           page:int,
                           limit:int,
                           search:str|None=None,
                           status:str|None=None
                           ):
          try:
            offset = (page-1)*limit
            
            getMyApplication , total = await self.applicationRepo.getMyApplication(
               applicant_id = user_id,
               offset=offset,
               limit=limit,
               search=search,
               status=status
          )
            
            total_pages=math.ceil(total/limit) if total > 0 else 0 
            
            
            if total == 0:
               raise CustomException("no applications found",status_code=404)

            if page > total_pages:
               raise CustomException(f"page {page} does not exist. total pages:{total_pages}",status_code=404)

            return{
               "data":getMyApplication,
               "pagination":{
                    "page":page,
                    "limit":limit,
                    "total":total,
                    "total_pages":total_pages
               }
          }

          except CustomException :
           raise

          except Exception as e:
           logger.error(f"my application erros:{str(e)}",exc_info=True)
          raise CustomException("unexcepted error occur",status_code=500)



