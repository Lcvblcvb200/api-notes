from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///banco.db")

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

class Notas(Base):
    __tablename__ = "notas"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nota = Column("nota", String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    def __init__(self, nota, usuario_id):
        self.nota = nota
        self.usuario_id = usuario_id
