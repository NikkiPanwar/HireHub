from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select 
from app.models.user import User

class UserRepository:

    def __init__(self, db: Session):
        self.db = db


    async def getAllUsers(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()


    async def getUsersById(self,userId:str):
        result = await self.db.execute(select(User).where(User.id == userId))
        return result.scalar_one_or_none()


    async def deleteUser(self,id:int):
        result = await self.db.execute(select(User).where(User.id == id))
        user =  result.scalar_one_or_none()

        if not user :
            return None 

        await self.db.delete(user)
        await self.db.commit()
        return user
    

    async def updateUser(self,user:User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user


    async def updateActiveUser(self,user:User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

            
