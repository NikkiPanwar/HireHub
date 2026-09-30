from fastapi import APIRouter ,Depends ,HTTPException,status
from app.schemas.user import (
    UserListResponse,
    UserDetailResponse,
    UpdateUser,
    UserResponse,
    UserAccountActiveRequest
)
from app.services.user_service import UserService
from app.exceptions.custom_exception import CustomException
from app.schemas.common import MessageResponse
from app.dependencies.auth import get_current_user


import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/getAllUsers",response_model=UserListResponse)
async def getAllUsers(user_service:UserService = Depends()):

    try :
        users = await user_service.getAllUsers()

        return UserListResponse(
            data = users,
            message = "users fetch successfully"
            )

    except CustomException as e:
        logger.error(f"Users error: {str(e)}", exc_info=True)

        raise HTTPException(
            status_code=e.status_code,
            detail=str(e)
        )

    except Exception as e:
        logger.error(f"Users details: {str(e)}", exc_info=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    
@router.get("/getAllUsers/{userId}",response_model=UserDetailResponse)
async def getUsersById(userId:int,
      user_service:UserService = Depends()
      ):

    try :
        user = await user_service.getUsersById(userId)

        return UserDetailResponse(
            data = user,
            message = "users fetch successfully"
            )

    except CustomException as e :
        logger.error(f"users error{str(e)}",exc_info=True)
        raise HTTPException(status_code=e.status_code,detail=str(e))

    except Exception as e :
        logger.error(f"users details:{str(e)}",exc_info=True)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error")
        
    
@router.delete("/deleteUser/{id}",response_model=MessageResponse)
async def deleteUser(
            id:int,
            user_service:UserService=Depends()
            ):
    try : 
        await user_service.deleteUser(id)

        return MessageResponse(
            message ="user delete succsessfully",
            data=None,
            success= True,
            status = status.HTTP_200_OK
        )

    except CustomException as e:
        logger.error(f"system user error :{str(e)}",exc_info=True)
        raise HTTPException(status_code=e.status_code,detail=str(e))

    except Exception as e :
        logger.error(f"delete details {str(e)}",exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
        )


@router.patch("/updateUser/{id}", response_model=MessageResponse[UserResponse], status_code=status.HTTP_200_OK)
async def updateUser(
    id: int,
    payload: UpdateUser,
    user_service: UserService = Depends()
):
    try:
        updateData = await user_service.updateUserData(id, payload)

        return MessageResponse(
            data=UserResponse.model_validate(updateData),
            success=True,
            message="user updated successfully",
            status=status.HTTP_200_OK
        )

    except CustomException as e:
            logger.error(f"system user error :{str(e)}",exc_info=True)
            raise HTTPException(status_code=e.status_code,detail=str(e))
    
    except Exception as e :
            logger.error(f"user updates details {str(e)}",exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
            )


@router.patch("/updateActiveUser",response_model=MessageResponse[UserResponse],
              status_code=status.HTTP_200_OK)

async def updateActiveUser(
     payload: UserAccountActiveRequest,
     current_user = Depends(get_current_user),
     user_service:UserService = Depends()
):
     try :
          updatedActiveUser = await user_service.updateActiveUser(payload,current_user)

          return MessageResponse(
               data = UserResponse.model_validate(updatedActiveUser),
               message = f"user {'active successfully' if payload.is_active else 'deactive'} successfully",
               success=True,
               status = status.HTTP_200_OK
          )

     except CustomException as e :
           logger.error(f"system user error :{str(e)}",exc_info=True)
           raise HTTPException(status_code=e.status_code,detail=str(e))
              
     except Exception as e :
             logger.error(f"user updates details {str(e)}",exc_info=True)
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail="Internal server error")
          
     


