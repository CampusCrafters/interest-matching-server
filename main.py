import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import requests
from fastapi.responses import JSONResponse

app = FastAPI()
load_dotenv()
PORT = os.getenv('PORT')
VERIFY_TOKEN_API = os.getenv('VERIFY_API')

@app.get('/users')
def getAllUsers(request: Request):
    token = request.cookies.get('jwt')
    if not token:
        return JSONResponse(
            status_code=400,
            content={'message': 'No token provided in the request'}
        )
    
    user = authenticateUser(token)
    if user:
        return JSONResponse(content={'message': 'Success', 'decoded': user})
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

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv('PORT'))
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)
