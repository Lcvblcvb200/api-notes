from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema, LoginSchema
from database import sessao
from sqlalchemy.orm import Session
from models import Usuario
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS
from jose import jwt
from datetime import datetime, timedelta, timezone

authrouter = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(iduser, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": iduser, "exp": data_expiracao}
    token = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return token

def autenticar(senha, email, session):
    busca = session.query(Usuario).filter(Usuario.email == email).first()
    if not busca:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    elif not bcrypt_context.verify(senha, busca.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return busca

@authrouter.post("/cadastrar")
async def cadastro(body: UserSchema, session : Session = Depends(sessao)):
    queryuser = session.query(Usuario).filter(Usuario.email == body.email).first()
    if queryuser:
        raise HTTPException(status_code=401, detail="Esse Usuário já existe")
    else:
        senha_cript = bcrypt_context.hash(body.senha)
        novo_user = Usuario(body.nome, body.email, senha_cript)
        session.add(novo_user)
        session.commit()
        return(f"Bem vindo {novo_user.nome}")
    
@authrouter.post("/login")
async def logar(body: LoginSchema, session: Session = Depends(sessao)):
    usuario_autenticado = autenticar(body.senha, body.email, session)
    access_token = criar_token(usuario_autenticado.id)
    return{
        "access_token": access_token,
        "token_type": "Bearer"
    }