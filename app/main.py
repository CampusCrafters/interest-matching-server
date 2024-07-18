import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from app.middleware.authMiddleware import authMiddleware
from app.routes.user_routes import user_router
from app.routes.match_routes import match_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

app.include_router(user_router)
app.include_router(match_router)

SWAGGER_UI_PATHS = {"/docs", "/openapi.json", "/redoc"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.middleware('http')
async def authenticationMiddleware(request: Request, call_next):
    if request.url.path in SWAGGER_UI_PATHS:
        response = await call_next(request)
        return response
    
    response = await authMiddleware(request, call_next)
    return response

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv('PORT')) 
    uvicorn.run("app.main:app", host="127.0.0.1", port=PORT, reload=True)
