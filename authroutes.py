from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from schemas import UserSchema, LoginSchema
from database import sessao
from sqlalchemy.orm import Session
from models import Usuario
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

authrouter = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def criar_token(iduser, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(iduser), "exp": data_expiracao}
    token = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return token

def token_verify(token: str = Depends(oauth2_scheme), session: Session = Depends(sessao)):
    try:
        decodified_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid = decodified_token.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    user = session.query(Usuario).filter(Usuario.id == userid).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user

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

@authrouter.get("/perfil")
async def ver_perfil(usuario: Usuario = Depends(token_verify)):
    return {"nome": usuario.nome, "email": usuario.email}