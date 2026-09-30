from fastapi import APIRouter, Depends, HTTPException, status ,Query
from app.schemas.application import ApplicationCreate, ApplicationCreateResponse,AllApplicationResponse,DeleteResponseWrapper,ApplicationResponseWrapper,UpdateApplicationResponse,ApplicationUpdate,ApplicationStatusResponse,ApplicationStatusUpdate,MyApplicationsResponse,MyApplicationsResponseWrapper
from app.services.application_service import ApplicationService
from app.exceptions.custom_exception import CustomException
from app.dependencies.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post(
    "/create-applications",
    response_model=ApplicationCreateResponse,
    status_code=status.HTTP_201_CREATED
)
@router.post(
    "",
    response_model=ApplicationCreateResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
async def createApplication(
    payload: ApplicationCreate,
    current_user = Depends(get_current_user),
    application_service: ApplicationService = Depends()
):
    try:
        applicationData = await application_service.createApplication(payload, current_user.id)

        return ApplicationCreateResponse(
            data=applicationData,
            message="Application created successfully",
            success=True
        )

    except CustomException as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=e.status_code, detail=str(e))

    except Exception as e:
        logger.error(f"System error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/getApplications",response_model=AllApplicationResponse)
async def getApplications(
      page:int = Query(1,ge=1),
      limit:int = Query(10,ge=1,le=100),
      search:str|None=Query(None),
      application_status:str|None=Query(None),
    application_service:ApplicationService = Depends()
):
    try :
        getApplication = await application_service.getApplications(
              page=page,
              limit=limit,
              search=search,
              application_status=application_status
        )

        return AllApplicationResponse(
            data = getApplication["data"],
            pagination=getApplication["pagination"],
            message='applications fetch successfully',
            success=True
        )

    except CustomException as e:
            logger.error(f"Application error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
            logger.error(f"System error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


@router.get("/getApplicationsById/{application_id}",response_model=ApplicationResponseWrapper)
async def getApplicationsById(
     application_id:int,
    application_service:ApplicationService = Depends()
):
    try :
        getApplicationById = await application_service.getApplicationById(application_id)

        return ApplicationResponseWrapper(
            data = getApplicationById,
            message='applications fetch successfully',
            success=True
        )

    except CustomException as e:
            logger.error(f"Application error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
            logger.error(f"System error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


@router.delete("/deleteApplicationsById/{deleteId}",response_model=DeleteResponseWrapper)
async def deleteApplicationsById(
     deleteId:int,
    application_service:ApplicationService = Depends()
):
    try :
        await application_service.deleteApplicationById(deleteId)

        return DeleteResponseWrapper(
            data = None,
            message='applications deleted successfully',
            success=True
        )

    except CustomException as e:
            logger.error(f"Application delete error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
            logger.error(f"System error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

@router.patch("/updateApplicationsById/{updateId}",response_model=UpdateApplicationResponse)
async def updateApplicationsById(
     updateId:int,
     payload:ApplicationUpdate,
    application_service:ApplicationService = Depends()
):
    try :
        updateApplication = await application_service.updateApplicationById(updateId,payload)

        return UpdateApplicationResponse(
            data = updateApplication,
            message='applications updated successfully',
            success=True
        )

    except CustomException as e:
            logger.error(f"Application update error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
            logger.error(f"System error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    

@router.patch("/updateApplicationStatus/{updateId}",response_model=ApplicationStatusResponse)
async def updateApplicationsStatus(
     updateId:int,
     payload:ApplicationStatusUpdate,
    application_service:ApplicationService = Depends()
):
    try :
        updateApplication = await application_service.updateApplicationStatus(updateId,payload.status.value)

        return ApplicationStatusResponse(
            data = updateApplication,
            message='applications status successfully',
            success=True
        )

    except CustomException as e:
            logger.error(f"Application status error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
            logger.error(f"System error with status: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    

@router.get("/my-applications",response_model=MyApplicationsResponseWrapper)
async def myApplications(
      page:int=Query(1,ge=1),
      limit:int=Query(10,ge=1,le=100),
      search:str|None=None,
      status:str|None=None,
      current_user = Depends(get_current_user),
      application_service:ApplicationService = Depends()
)  :
      try :
            myApplications = await application_service.getMyApplication(
                  user_id=current_user.id,
                  page=page,
                  limit=limit,
                  search=search,
                  status=status
            )

            return MyApplicationsResponseWrapper(
                  data = myApplications["data"],
                  pagination = myApplications["pagination"],
                  message="users applications fetch successfully"
            )
      except CustomException as e:
            logger.error(f"my applications error:{str(e)}",exc_info=True)
            raise HTTPException(status_code=e.status_code,detail=str(e))

      except Exception as e:
            logger.error(f"system error:{str(e)}",exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong while fecthing my applications")
      









