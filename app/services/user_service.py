from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.exceptions.custom_exception import CustomException
from app.config.database import get_db
from app.repositories.user_repository import UserRepository
from typing import Dict
from app.schemas.user import UpdateUser
from app.schemas.user import UserAccountActiveRequest


import logging 

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self,db:AsyncSession=Depends(get_db)):
        self.userRepo = UserRepository(db)


    async def getAllUsers(self)->Dict:
        try :
            allUsers = await self.userRepo.getAllUsers()

            if not allUsers :
                raise CustomException("users data not found",status_code=404)

            return allUsers

        except CustomException :
            raise 

        except Exception as e:
            logger.error(f"user details api issues:{str(e)}",exc_info=True)
            raise


    async def getUsersById(self,userId:str)->Dict:
             try :
                 allUsers = await self.userRepo.getUsersById(userId)
     
                 if not allUsers :
                     raise CustomException("users data not found",status_code=404)
     
                 return allUsers
     
             except CustomException :
                 raise 
     
             except Exception as e:
                 logger.error(f"user details api issues:{str(e)}",exc_info=True)
                 raise
                        

    async def deleteUser(self,id:int)->Dict:
        try :
            if not id :
                raise CustomException("delete id not found")

            checkUser = await self.userRepo.deleteUser(id)

            if not checkUser :
                raise CustomException("user not found")

            return checkUser

        except CustomException as e :
            logger.error(f"delete services error:{str(e)}",exc_info=True)
            raise 


    async def updateUserData(
            self,
            id: int,
            payload: UpdateUser
    ):
        try:
            if not id:
                raise CustomException("id not found", status_code=400)

            checkUser = await self.userRepo.getUsersById(id)

            if not checkUser:
                raise CustomException("user not found", status_code=404)

            new_username = payload.username or payload.user_name

            if payload.email is None and payload.full_name is None and new_username is None:
                raise CustomException("At least one field is required to update", status_code=400)

            if payload.email is not None:
                checkUser.email = payload.email
            if new_username is not None:
                checkUser.username = new_username
            if payload.full_name is not None:
                checkUser.full_name = payload.full_name

            return await self.userRepo.updateUser(checkUser)

        except IntegrityError:
            await self.userRepo.db.rollback()
            raise CustomException("Email or username already exists", status_code=400)

        except CustomException as e:
            logger.error(f"system error: {str(e)}", exc_info=True)
            raise



    async def updateActiveUser(self,payload:UserAccountActiveRequest,current_user)->Dict:
        try :
            if not current_user :
                raise CustomException("user id not found",status_code=404)

            if payload.is_active is None :
                raise CustomException("this is required",status_code=404)

            current_user.is_active = payload.is_active

            return await self.userRepo.updateActiveUser(current_user)

        except CustomException :
            raise 

        except Exception as e:
            logger.error(f"user active status:{str(e)}",exc_info=True)
            raise 

               

        
