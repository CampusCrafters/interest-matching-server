import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from prisma import Prisma

load_dotenv()

BACKEND_API = os.getenv('BACKEND_API')

user_router = APIRouter()

prisma = Prisma()

@user_router.get('/users')
async def get_all_usernames():
    await prisma.connect()
    try:
        # Fetch all users with specific fields selected
        users_with_names = await prisma.users.find_many()
        usernames = [user.name for user in users_with_names if user.name] 
        return usernames
    except Exception as e:
        print(f"Error fetching user names: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user names")
