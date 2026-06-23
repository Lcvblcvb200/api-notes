from sqlalchemy.orm import sessionmaker
from models import db

Session = sessionmaker(bind=db)

def sessao():
    try:
        session = Session()
        yield session
    finally:
        session.close()