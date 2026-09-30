from fastapi import APIRouter ,Depends ,HTTPException ,status ,Query
from app.schemas.job import JobCreateResponse,JobCreate,AllJobResponse,JobUpdate,UpdateJobResponse,JobResponse,JobStatusUpdate
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

from app.services.job_service import JobService
from app.exceptions.custom_exception import CustomException
from app.schemas.common import MessageResponse

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs",tags=["Jobs"])

@router.post("/create-jobs",
             response_model=JobCreateResponse,
             status_code=status.HTTP_201_CREATED
             )
async def createJob(
    payload:JobCreate,
    current_user=Depends(get_current_user),
    job_service:JobService =Depends()
):
     try :
          create_job = await job_service.createJob(payload,current_user.id)

          return JobCreateResponse(
               data = create_job,
               message ="job created successfully",
               success=True
          )

     except CustomException as e :
          logger.error(f"create job errors:{str(e)}")
          raise HTTPException(status_code=e.status_code, detail=str(e))

     except Exception as e :
          logger.error(f"system error:{str(e)}",exc_info=True)
          raise HTTPException( 
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="something went wrong while creating job"
          )


@router.get("/all-jobs",
            response_model=AllJobResponse,
            status_code=status.HTTP_200_OK
            )
async def getAllJobs(
     page:int = Query(1,ge=1),
     limit:int = Query(10,ge=1,le=100),
     search:str|None = Query(None),
     job_type:str|None = Query(None),
     location:str|None = Query(None),
     is_active:bool|None =Query(None),
     job_service:JobService = Depends()
     ):

     try :
          getJobData = await job_service.getAllJobs(
               page=page,
               limit=limit,
               search=search,
               job_type=job_type,
               location=location,
               is_active=is_active
               )

          return AllJobResponse(
          data = getJobData["data"],
          pagination=getJobData["pagination"],
          message="fetch jobs successfully",
          success=True
         )

     except CustomException as e :
          logger.error(f"user error:{str(e)}",exc_info=True)
          raise HTTPException(status_code=e.status_code, detail=str(e))

     except Exception as e:
          logger.error(f"system error:{str(e)}",exc_info=True)
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong while fetching job"
            )


@router.get("/getjobsById/{id}",
            response_model=JobCreateResponse,
            status_code=status.HTTP_200_OK
            )
async def getJobsById(
     id:int,
     job_service:JobService = Depends()
     ):

     try :
          getJobDataById = await job_service.getAllJobsById(id)

          return JobCreateResponse(
          data = getJobDataById,
          message="fetch jobs successfully",
          success=True
         )

     except CustomException as e :
          logger.error(f"user error:{str(e)}",exc_info=True)
          raise HTTPException(status_code=e.status_code, detail=str(e))

     except Exception as e:
          logger.error(f"system error:{str(e)}",exc_info=True)
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong while fetching job"
            )


@router.delete("/delete/{id}",
            response_model=MessageResponse,
            status_code=status.HTTP_200_OK
            )
async def deleteJob(
     id:int,
     job_service:JobService = Depends()
     ):

     try :
          await job_service.deletJobId(id)

          return MessageResponse(
          data = None,
          message="jobs deleted successfully",
          success=True,
          status=200
         )

     except CustomException as e :
          logger.error(f"user error:{str(e)}",exc_info=True)
          raise HTTPException(status_code=e.status_code, detail=str(e))

     except Exception as e:
          logger.error(f"system error:{str(e)}",exc_info=True)
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong while fetching job"
            )


@router.patch("/updateJob/{id}",
              response_model=UpdateJobResponse,
              status_code=status.HTTP_200_OK
             )
async def updateJob(id:int,
                    payload:JobUpdate,
                    job_service:JobService=Depends()
                  ):
     try:

          updateData = await job_service.updateJob(id,payload)

          return UpdateJobResponse(
               data = updateData,
               message = "job data updated successfully",
               success=True
          )
     
     except CustomException as e :
          logger.error(f"user update job issues:{str(e)}",exc_info=True)
          raise HTTPException(status_code=e.status_code,detail=str(e))

     except Exception as e :
          logger.error(f"system errors:{str(e)}",exc_info=True)
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail="internal server error"
     )



@router.patch("/activeStatus/{id}",response_model=UpdateJobResponse)

async def updateJobActiveStatus(
     id:int,
     payload:JobStatusUpdate,
     job_service:JobService=Depends()
):
     try :
          updatedActiveJobData = await job_service.updatedActiveData(id,payload)
          return UpdateJobResponse(
               data = updatedActiveJobData ,
               message =f"job {'opened' if payload.is_active else 'closed'} succssfully",success=True
          )
     
     except CustomException as e :
          raise HTTPException(status_code=e.status_code,detail=str(e))

     except Exception as e :
          logger.error(f"error updating job status:{str(e)}",exc_info=True)
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="INERNAL SERVER ERROR")

