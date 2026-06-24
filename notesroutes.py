from fastapi import APIRouter, Depends, HTTPException
from database import sessao
from sqlalchemy.orm import Session
from models import Notas, Usuario
from schemas import NotaSchema
from authroutes import token_verify

noterouter = APIRouter(prefix="/note", tags=["notes"])

@noterouter.post("/create")
async def create_note(body: NotaSchema, usuario: Usuario = Depends(token_verify), session: Session = Depends(sessao)):
    note = Notas(body.nota, usuario_id=usuario.id)
    session.add(note)
    session.commit()
    return{"mensagem": "Nota Criada"}

@noterouter.get("/")
async def view_notes(usuario: Usuario = Depends(token_verify), session: Session = Depends(sessao)):
    notes = session.query(Notas).filter(Notas.usuario_id == usuario.id).all()
    return notes
