from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import (
    UserCreate,
    AuthRegisterResponse,
    UserLogin,
    UserListResponse,
    Token,
    UserDetailResponse,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
    UserResponse
)
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService
from app.exceptions.custom_exception import CustomException
import logging
from app.dependencies.auth import get_current_user



logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthRegisterResponse, status_code=status.HTTP_201_CREATED)
async def createUser(
    payload: UserCreate,
    auth_service: AuthService = Depends()
):
    try:
        create_data = await auth_service.createUser(payload)
        return AuthRegisterResponse(
            user=create_data["user"],
            access_token=create_data["access_token"],
            token_type=create_data["token_type"],
            refresh_token=create_data["refresh_token"],
            message="User registered successfully"
        )
    except CustomException as e:
        logger.error(f"User registration error: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"System error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while registering the user"
        )


@router.post("/login",response_model=AuthRegisterResponse,
             status_code=status.HTTP_200_OK)
async def login(payload:UserLogin,
                auth_service:AuthService = Depends()):

    try : 
        login_user = await auth_service.login_user(payload)
        return AuthRegisterResponse(
            user = login_user["user"],
            access_token=login_user["access_token"],
            token_type=login_user["token_type"],
            refresh_token=login_user["refresh_token"],
            message="User login successfully"
        )

    except CustomException as e:
            logger.error(f"User login error: {str(e)}")
            raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
            logger.error(f"System error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong while login"
            )


@router.get("/allUsersDetail",response_model=UserListResponse)   
async def userDetail(auth_service:AuthService=Depends()):
     try :
          getUsersDetails = await auth_service.getUserDetails()

          return UserListResponse(
               data = getUsersDetails,
                message = "user details fetch successfully"
          )

     except CustomException as e:
                 logger.error(f"User details error: {str(e)}")
                 raise HTTPException(status_code=e.status_code, detail=str(e))
     
     except Exception as e:
                 logger.error(f"user details error: {str(e)}", exc_info=True)
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong while fetching user info")

    
@router.get("/usersDetail/{user_id}",response_model=UserDetailResponse)   
async def userDetail(user_id:int,auth_service:AuthService=Depends()):
     try :
          getUsersDetails = await auth_service.getUserDetailsById(user_id)

          return UserDetailResponse(
               data = getUsersDetails,
                message = "user details fetch successfully"
          )

     except CustomException as e:
                 logger.error(f"User details error: {str(e)}")

                 raise HTTPException(status_code=e.status_code, detail=str(e))
     
     except Exception as e:
                 logger.error(f"user details error: {str(e)}", exc_info=True)
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong while fetching user info")


@router.post("/refresh-token",response_model=Token)
async def refreshToken(
       payload:RefreshTokenRequest,
       auth_service:AuthService = Depends()
       ):
       try :
              checkData = await auth_service.tokenData(payload)
              return Token(
                    access_token = checkData["access_token"],
                    refresh_token= checkData["refresh_token"],
                    token_type=checkData["token_type"],
                    message ="token refresh successfully"   
              )
       
       except CustomException as e:
        logger.error(f"Refresh token error: {str(e)}")

        raise HTTPException(status_code=e.status_code,detail=str(e))

       except Exception as e:
        logger.error(f"System error: {str(e)}",exc_info=True)

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while refreshing token"
        )


@router.post("/logout",response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def logout(auth_service:AuthService = Depends()):
      try:
            await auth_service.logout_user()
            return MessageResponse(message="successfully logged out")

      except CustomException as e :
        logger.error(f"logout error:{str(e)}")
        raise HTTPException(status_code=e.status_code,detail=str(e))

      except Exception as e :
        logger.error(f"system error:{str(e)}",exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Something went wrong while logout")



@router.post("/forgotPassword")
async def forgotPassword(
    payload: ForgotPasswordRequest,
    auth_service: AuthService = Depends()
):
    try:
        data = await auth_service.forgotPassword(payload)
        return data
    
    except CustomException as e:
        logger.error(f"Forgot password error: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
        logger.error(f"System error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went wrong while processing forgot password")
    

@router.post("/resetPassword", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def resetPassword(
    payload: ResetPasswordRequest,
    auth_service: AuthService = Depends()
):
    try:
        data = await auth_service.resetPassword(payload)
        return MessageResponse(message=data["message"])
    
    except CustomException as e:
        logger.error(f"Reset password error: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
        logger.error(f"System error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went wrong while resetting password")    


@router.post("/changePassword", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def changePassword(
    payload: ChangePasswordRequest,
    auth_service: AuthService = Depends()
):
    try:
        data = await auth_service.changePassword(payload)
        return MessageResponse(message=data["message"])
    
    except CustomException as e:
        logger.error(f"Change password error: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
    except Exception as e:
        logger.error(f"System error: {str(e)}", exc_info=True)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while changing password"
        )

     
                     
@router.get("/auth/me",response_model=UserDetailResponse,status_code=status.HTTP_200_OK)    
async def myProfile(
        current_user=Depends(get_current_user),
        auth_service:AuthService = Depends()
):
     try :
          myData= await auth_service.userProfile(current_user)

          return UserDetailResponse(
               data = myData,
               message = "profile api call successfully executed"
          )    

     except CustomException as e:
          logger.error(f"user profile api call:{str(e)}",exc_info=True)
          raise HTTPException(status_code=e.status_code,detail=str(e))

     except Exception as e:
          logger.error(f"user profile issue:{str(e)}",exc_info=True)
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          DETAIL="SOME thing went wrong")
     
     
     

         
     
        
        