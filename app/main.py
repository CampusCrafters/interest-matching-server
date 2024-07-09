import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from app.middleware.authMiddleware import authMiddleware
from app.routes.user_routes import user_router

app = FastAPI()
load_dotenv()

app.include_router(user_router)

@app.middleware('http')
async def authenticationMiddleware(request: Request, call_next):
    return await authMiddleware(request, call_next)

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv('PORT'))
    uvicorn.run("app.main:app", host="127.0.0.1", port=PORT, reload=True)
