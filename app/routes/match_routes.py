from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from prisma import Prisma

match_router = APIRouter()

prisma = Prisma()

@match_router.post('/like/{liked_user_id}')
async def like_user(liked_user_id: int, request: Request):
    try:
        await prisma.connect()

        user_email = request.state.user['email']
        print(user_email)
        user_id = (await prisma.users.find_unique(where={'email': user_email})).user_id
        print(f'userid: ${user_id}')
        if liked_user_id == user_id:
            return JSONResponse(
                status_code=400,
                content={'message': 'You cannot like yourself'}
            )
        elif liked_user_id not in [user.user_id for user in await prisma.users.find_many()]:
            return JSONResponse(
                status_code=404,
                content={'message': 'User not found'}
            )
        if await prisma.likes.find_first(where={'user_id': user_id, 'liked_user_id': liked_user_id}):
            return JSONResponse(
                status_code=400,
                content={'message': 'User already liked'}
            )
        
        await prisma.likes.create(data={'user_id': user_id, 'liked_user_id': liked_user_id})
        print(f'liked_user_id: {liked_user_id}')
        matched_user = await prisma.likes.find_first(
            where={'user_id': liked_user_id, 'liked_user_id': user_id}
        )
        if matched_user:
            await prisma.matches.create(data={
                'user1_id': user_id,
                'user2_id': liked_user_id
            })
            return JSONResponse(
                status_code=200,
                content={'message': 'It\'s a match!'}
            )
        elif matched_user is None:
            return JSONResponse(
                status_code=200,
                content={'message': 'User liked successfully, We will notify you if it\'s a match'}
            )
        return JSONResponse(
            status_code=200,
            content={'message': 'User liked successfully, We will notify you if it\'s a match'}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'message': 'Error liking user', 'error': str(e)}
        )
    finally:
        await prisma.disconnect()
