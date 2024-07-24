from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from prisma import Prisma

user_router = APIRouter()

prisma = Prisma()

@user_router.get('/users')
async def get_all_users():
    await prisma.connect()
    try:
        users = await prisma.users.find_many()
        return users
    except Exception as e:
        print(f"Error fetching user names: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user names")
    finally:
        await prisma.disconnect()


@user_router.get('/likedUsers')
async def get_liked_users(request: Request):
    await prisma.connect()

    try:
        user_email = request.state.user['email']
        user_id = (await prisma.users.find_unique(where={'email': user_email})).user_id

        liked_user_ids = [like.liked_user_id for like in await prisma.likes.find_many(where={'user_id': user_id})]
        liked_users = await prisma.users.find_many(
            where={'user_id': {'in': liked_user_ids}},
        )
        filtered_users = [
            {
            'user_id': user.user_id,
            'profile_picture': user.profile_picture,
            'name': user.name
            }
            for user in liked_users
        ]

        return filtered_users
    finally:
        await prisma.disconnect()


@user_router.get('/matchedUsers')
async def get_matched_users(request: Request):
    await prisma.connect()

    try:
        user_email = request.state.user['email']
        user_id = (await prisma.users.find_unique(where={'email': user_email})).user_id

        matches = await prisma.matches.find_many(where={
            'OR': [
                {'user1_id': user_id},
                {'user2_id': user_id}
            ]
        })
        matched_user_ids = [match.user1_id if match.user2_id == user_id else match.user2_id for match in matches]
        matched_users = await prisma.users.find_many(where={'user_id': {'in': matched_user_ids}})

        filtered_users = [
            {
            'user_id': user.user_id,
            'profile_picture': user.profile_picture,
            'name': user.name
            }
            for user in matched_users
        ]
        return filtered_users

    except Exception as e:
        print(f"Error fetching matched users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching matched users")
    finally:
        await prisma.disconnect()
