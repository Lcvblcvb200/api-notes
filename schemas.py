from pydantic import BaseModel

class UserSchema(BaseModel):
    nome: str
    email: str
    senha: str

class NotaSchema(BaseModel):
    nota: str