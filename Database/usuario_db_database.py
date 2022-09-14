from sqlalchemy import Integer, String, Date, text, Boolean, SmallInteger
from sqlalchemy.sql.schema import Column
from Database.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50))