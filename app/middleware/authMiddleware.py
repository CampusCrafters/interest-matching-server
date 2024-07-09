import os
from fastapi import Request
from fastapi.responses import JSONResponse
import requests

VERIFY_TOKEN_API = os.getenv('VERIFY_API')

async def authMiddleware(request: Request, call_next):
    token = request.cookies.get('jwt')
    if not token:
        return JSONResponse(
            status_code=400,
            content={'message': 'No token provided in the request'}
        )
    user = authenticateUser(token)
    if user:
        request.state.user = user  # Store user data in request state
        response = await call_next(request)
        return response
    else:
        return JSONResponse(
            status_code=401,
            content={'message': 'Token verification failed'}
        )

def authenticateUser(token: str):
    try:
        response = requests.post(
            VERIFY_TOKEN_API,
            headers={'Content-Type': 'application/json'},
            json={'token': token}
        )
        response.raise_for_status()
        return response.json().get('decoded')
    except requests.RequestException as e:
        print(f"Error in authenticateUser: {e}")
        return None
