from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema 
from database import sessao
from sqlalchemy.orm import Session
from models import Usuario
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

authrouter = APIRouter(prefix="/auth", tags=["auth"])

@authrouter.post("/cadastrar")
async def cadastro(body: UserSchema, session : Session = Depends(sessao)):
    queryuser = session.query(Usuario).filter(Usuario.email == body.email)
    if queryuser:
        raise HTTPException(status_code=401, detail="Esse Usuário já existe")
    else:
        senha_cript = bcrypt_context(body.senha)