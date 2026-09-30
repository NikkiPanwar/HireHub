from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select , or_ 
from app.schemas.user import UserCreate ,ResetPasswordRequest
from app.models.user import User
from sqlalchemy.orm import selectinload


class AuthRepository:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def checkEmail(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


    async def checkUsername(self, username: str):
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()


    async def createUser(self, payload: UserCreate, hashed_pwd: str):
        role_value = payload.role.value if hasattr(payload.role, "value") else str(payload.role)
        newUser = User(
            email=payload.email,
            username=payload.username,
            full_name=payload.full_name,
            role=role_value,
            hashed_password=hashed_pwd
        )

        self.db.add(newUser)
        await self.db.commit()
        await self.db.refresh(newUser)
        return newUser
    

    async def checkNewLoginUser(self, username_or_email:str):
        result = await self.db.execute(select(User).where(
            or_(
        User.email == username_or_email, 
        User.username == username_or_email
            )
        )
    )
        return result.scalar_one_or_none()


    async def getUsersDetails(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()


    async def getUsersDetailsById(self,user_id:int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


    async def getUserById(self,user_id:int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


    async def forgotPasswordCheck(self,email:str):
        result =await self.db.execute(select(User).where(or_(User.email == email)))
        return result.scalar_one_or_none()


    async def addPassword(self,payload:ResetPasswordRequest,new_hash_password:str):
        user = await self.checkEmail(payload.email)
        if not user :
            return None

        user.hashed_pwd = new_hash_password 
        await self.db.commit()
        await self.db.refresh(user)
        return user


    async def updateUserPassword(self,email:str,new_hashed_password:str):

        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalaar_one_or_none()

        if not user :
            return None 

        user.hashed_pwd = new_hashed_password
        await self.db.commit()
        await self.db.refresh(user)
        return user

    
    async def userProfileData(self,current_user:int):
        result = await self.db.execute(select(User).options(selectinload(User.jobs)).where(User.id == current_user.id))
        return result.scalar_one_or_none()
        



