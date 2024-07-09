from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from prisma import Prisma

match_router = APIRouter()

prisma = Prisma()

@match_router.post('/like/{liked_user_id}')
async def like_user(liked_user_id: int, request: Request):
    await prisma.connect()

    user_email = request.state.user['email']
    user_id = (await prisma.users.find_unique(where={'email': user_email})).user_id

    if liked_user_id == request.state.user['user_id']:
        return JSONResponse(
            status_code=400,
            content={'message': 'You cannot like yourself'}
        )
    elif liked_user_id not in [user.user_id for user in await prisma.users.find_many()]:
        return JSONResponse(
            status_code=404,
            content={'message': 'User not found'}
        )
    
    try:
        await prisma.likes.create(data={'user_id': user_id, 'liked_user_id': liked_user_id})
        return JSONResponse(
            status_code=200,
            content={'message': 'User liked successfully'}
        )
    except Exception as e:
        print(f"Error liking user: {e}")
        return JSONResponse(
            status_code=500,
            content={'message': 'Error liking user'}
        )
    finally:
        await prisma.disconnect()
