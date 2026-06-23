from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

bcrypt_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

app = FastAPI()

from authroutes import auth_router
from notaroutes import nota_router

app.include_router(auth_router)
app.include_router(nota_router) 