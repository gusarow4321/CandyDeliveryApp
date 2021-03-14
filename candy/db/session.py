from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session(db_url):
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
