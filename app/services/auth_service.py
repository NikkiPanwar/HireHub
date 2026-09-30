from typing import Dict 
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.custom_exception import CustomException
from app.config.database import get_db
from app.repositories.auth_repository import AuthRepository
from app.schemas.user import UserCreate ,UserLogin ,RefreshTokenRequest,ForgotPasswordRequest,ResetPasswordRequest,ChangePasswordRequest
from app.core.security import create_access_token ,hash_password , verify_password ,verify_refresh_token,create_refresh_token,create_password_reset_token,verify_password_reset_token



import logging

logger= logging.getLogger(__name__)

class AuthService:


    def __init__(self,db:AsyncSession = Depends(get_db)):
        self.authRepo = AuthRepository(db)


    async def createUser(
            self,
            payload:UserCreate
    )->Dict :

         try :

            if not payload.email or not payload.username or not payload.full_name or not payload.role:
                raise CustomException("All fields are required")

            check_email = await self.authRepo.checkEmail(payload.email)
            if check_email:
                raise CustomException("User with this email already exists")

            check_username = await self.authRepo.checkUsername(payload.username)
            if check_username:
                raise CustomException("User with this username already exists")


            hashed_pwd = hash_password(payload.password)
            new_data = await self.authRepo.createUser(payload, hashed_pwd)

            access_token = create_access_token(
                data={
                "sub": str(new_data.id), 
                "role":new_data.role}
            )

            refresh_token = create_refresh_token(
                data ={
                    "sub":str(new_data.id),
                    "role":new_data.role
                }
            )

            return{
            "user" : new_data ,
            "access_token":access_token,
            "refresh_token":refresh_token,
            "token_type":"bearer"
            }

         except CustomException:
            raise

         except Exception as e:
            logger.error(f"User service error: {str(e)}",exc_info=True)

            raise CustomException("Unexpected error while creating user",status_code=500)


    async def login_user(self,payload:UserLogin)->Dict :
        try :
            if not payload.username_or_email or not payload.password:
                raise CustomException("password and email/username are required")

            check_data = await self.authRepo.checkNewLoginUser(payload.username_or_email)

            if not check_data :
                raise CustomException("invalid email/username or password")

            password_valid = verify_password(payload.password,check_data.hashed_password)

            if not password_valid:
                raise CustomException("invalid username/email or password")

            if not check_data.is_active:
                raise CustomException("user account is not active")

            
            access_token = create_access_token(
                data ={
                    "sub":str(check_data.id),
                    "role":check_data.role
                }
            )

            refresh_token = create_refresh_token(
                data={
                    "sub":str(check_data.id),
                    "role":check_data.role
                }
            )

            return {
                "user":check_data,
                "access_token":access_token,
                "refresh_token":refresh_token,
                "token_type":"bearer"
            }

        except CustomException:
            raise 

        except Exception as e :
            logger.error(f"user login error:{str(e)}",exc_info=True)
            raise CustomException("unexcepted error occured while login",status_code=500)


    async def getUserDetails(self)->Dict:
        try :
            getUserData = await self.authRepo.getUsersDetails()  

            if not getUserData :
                raise CustomException("data not found")
            
            return getUserData

        except CustomException as e:
            raise 

        except Exception as e:
            logger.error(f"error while fetching users:{str(e)}",exc_info=True)

            raise CustomException(f"unexcepted error ocurre while fetching the users details",status_code=500)


    async def getUserDetailsById(self,user_id:int)->Dict:
        try :
            getUserData = await self.authRepo.getUsersDetailsById(user_id)  

            if not getUserData :
                raise CustomException("data not found")
            
            return getUserData

        except CustomException as e:
            raise 

        except Exception as e:
            logger.error(f"error while fetching users:{str(e)}",exc_info=True)

            raise CustomException(f"unexcepted error ocurre while fetching the users details",status_code=500)


    async def tokenData(self,payload:RefreshTokenRequest)->Dict:
         try:

            if not payload.refresh_token:
                raise CustomException("token not found")


            token_payload = verify_refresh_token(payload.refresh_token)

            if not token_payload :
                raise CustomException("refresh token not found",status_code=404)

            user_id = token_payload.get("sub")

            checkData = await self.authRepo.getUserById(int(user_id))
            
            if not checkData :
                raise CustomException("user not found",status_code=401)

            if not checkData.is_active:
                raise CustomException("user acccount is inactive",status_code=403)
                        
            
            access_token  = create_access_token(
                data={
                    "sub":str(checkData.id),
                    "role":checkData.role,
                    "type":"access"
                    }
                )
            
            return {
            "access_token":access_token,
            "refresh_token":payload.refresh_token,
            "token_type":"bearer"
            }
            
         except CustomException :
            raise 
            
         except Exception as e :
            logger.error(f"refresh token error:{str(e)}",exc_info=True)
            
            raise CustomException("unexcepted error occur",status_code=500)
            

    async def logout_user(self):
        return True


    async def forgotPassword(self,payload:ForgotPasswordRequest)->Dict :
        try :
            if not payload.email:
                raise CustomException("email is required")            

            checkUser = await self.authRepo.forgotPasswordCheck(payload.email)

            if not checkUser :
                raise CustomException("user with this email is not found",status_code=404)

            reset_token = create_password_reset_token(payload.email)
        
            return {
                "email":checkUser.email,
                "message":"email exits",
                "reset_token":reset_token
            }

        except CustomException :
            raise 

        except Exception as e :
            logger.error(f"user forgot password error{str(e)}",exc_info=True)
            raise CustomException("Unexpected error while creating user",status_code=500)


    async def resetPassword(self,payload:ResetPasswordRequest)->Dict:
        try :
            if not payload.new_password or not payload.token :
                raise CustomException("password and token are required")

            email = verify_password_reset_token(payload.token)

            if not email :
                raise CustomException("invalid or wrong email or token",status_code=400)

            new_hashed_pwd  = hash_password(payload.new_password)                     

            updatePassword = await self.authRepo.addPassword(payload.email ,new_hashed_pwd)

            if not updatePassword :
                raise CustomException("user not found",status_code=404)

            return {"message": "Password reset successfully"}

        except CustomException:
            raise

        except Exception as e:
            logger.error(f"Reset password error: {str(e)}", exc_info=True)
            raise CustomException("Unexpected error during password reset", status_code=500)


    async def changePassword(self,payload:ChangePasswordRequest)->Dict :
        try :

            if not payload.new_password or not payload.old_password or not payload.email:
                raise CustomException("all fields are required")

            user = await self.authRepo.checkEmail(payload.email)

            if not user :
                raise CustomException("user not found",status_code=404)

            if not verify_password(payload.old_password, user.hashed_password):
                 raise CustomException("old password is incorrect",status_code=400)

            if payload.new_password == payload.old_password:
             raise CustomException("new password must be different from old password",status_code=400)

            new_hashed_pwd = hash_password(payload.new_password)

            await self.authRepo.updateUserPassword(user.email,new_hashed_pwd)

            return {"message":"password chnages successfully"}

        except CustomException:
            raise

        except Exception as e:
            logger.error(f"Change password error: {str(e)}", exc_info=True)
            raise CustomException("Unexpected error while changing password", status_code=500)


    async def userProfile(self,current_user:int)->Dict:
        try :
            userData = await self.authRepo.userProfileData(current_user)

            if not userData:
                raise CustomException("user data not found",status_code=400)

            return userData

        except CustomException:
            raise

        except Exception as e :
            logger.error(f"user profile error:{str(e)}",exc_info=True)
            raise CustomException("unexcepted error while fetching data")   

            
            

            

