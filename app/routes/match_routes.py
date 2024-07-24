from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from prisma import Prisma

match_router = APIRouter()

prisma = Prisma()

@match_router.get('/like/{liked_user_id}')
async def like_user(liked_user_id: int, request: Request):
    try:
        await prisma.connect()

        user_email = request.state.user['email']
        user = await prisma.users.find_unique(where={'email': user_email})
        
        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        user_id = user.user_id
        
        if liked_user_id == user_id:
            raise HTTPException(status_code=400, detail='You cannot like yourself')

        liked_user = await prisma.users.find_unique(where={'user_id': liked_user_id})
        if not liked_user:
            raise HTTPException(status_code=404, detail='User not found')

        existing_like = await prisma.likes.find_first(where={'user_id': user_id, 'liked_user_id': liked_user_id})
        if existing_like:
            raise HTTPException(status_code=400, detail='User already liked')

        await prisma.likes.create(data={'user_id': user_id, 'liked_user_id': liked_user_id})
        
        matched_user = await prisma.likes.find_first(where={'user_id': liked_user_id, 'liked_user_id': user_id})
        
        if matched_user:
            await prisma.matches.create(data={'user1_id': user_id, 'user2_id': liked_user_id})
            return JSONResponse(status_code=200, content={'message': 'It\'s a match!'})
        
        return JSONResponse(status_code=200, content={'message': 'User liked successfully, We will notify you if it\'s a match'})
    
    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={'message': http_exc.detail})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': 'Error liking user', 'error': str(e)})
    
    finally:
        await prisma.disconnect()
