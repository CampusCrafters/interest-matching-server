import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from prisma import Prisma
from requests import request

load_dotenv()

BACKEND_API = os.getenv('BACKEND_API')

user_router = APIRouter()

prisma = Prisma()

@user_router.get('/users')
async def get_all_usernames():
    await prisma.connect()
    try:
        users = await prisma.users.find_many()
        return users
    except Exception as e:
        print(f"Error fetching user names: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user names")

@user_router.get('/likedUsers')
async def get_liked_users(request: Request):
    await prisma.connect()

    user_email = request.state.user['email']
    user_id = (await prisma.users.find_unique(where={'email': user_email})).user_id

    liked_users = await prisma.likes.find_many(where={'user_id': user_id})
    liked_user_id = [like.liked_user_id for like in liked_users]

    return JSONResponse(
        content={'user_id': user_id, 'liked_user_id': liked_user_id}
    )
