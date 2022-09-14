import email
from sqlalchemy import Integer, String, Date, text, Boolean, SmallInteger
from sqlalchemy.sql.schema import Column
from Database.database import Base

class Clientes(Base):
    __tablename__ = 'Clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(100))
    senha = Column(Integer)