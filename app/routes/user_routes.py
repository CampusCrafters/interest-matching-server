import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import requests
from prisma import Prisma

load_dotenv()

BACKEND_API = os.getenv('BACKEND_API')

user_router = APIRouter()

prisma = Prisma()

@user_router.get('/users')
async def getAllUsers(request: Request):
    await prisma.connect()
    # token = request.cookies.get('jwt')
    try:
        # response = requests.get(
        #     f"{BACKEND_API}/user/allUsers",
        #     headers={'Content-Type': 'Application/json', 'Cookie': f"jwt={token}"}
        # )
        users = prisma.users.find_many(select={'name'})
        return [users.name for user in users]

        # response.raise_for_status()
        # allUsers = response.json()
        # return JSONResponse(content={'users': allUsers})
    except requests.RequestException as e:
        print(f"Error in getting all users: {e}")
        return JSONResponse(
            status_code=500,
            content={'message': 'Error fetching users'}
        )
    