from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ProjectMain import settings




def get_db_engine():

    return create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def get_db_session():
    engine = get_db_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)



def get_db():
    db_session = get_db_session()
    db = db_session()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()


def create_tables():
    # Must import all models created in the future
    from books import models
    from auth import models
    Base.metadata.create_all(bind=get_db_engine())