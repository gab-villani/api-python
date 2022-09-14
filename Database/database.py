from pytz import timezone
import pytz
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:123@127.0.0.1:5432/gabrielaAprendizagem"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"options": "-c timezone=America/Campo_Grande"})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()