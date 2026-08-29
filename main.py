from fastapi import FastAPI
from dotenv import load_dotenv
from user.userController import router as user_router

app = FastAPI(title="BrazilMart", description="E-commerce open-source APIs", version="1.0.0")
app.include_router(user_router)
@app.get('/')
async def root():
    return {'message': 'Welcome to the BrazilMart!'}