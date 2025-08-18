from fastapi import FastAPI
from app.services.Text_Video.video_route import router
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

app = FastAPI()

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Text-to-Video API is running!"}