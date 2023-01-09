from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import settings

SQLITE_URI = 'sqlite:///./src/apidata.db'
MYSQL_URI = f'mysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

if (settings.debugging):
    engine = create_engine(SQLITE_URI, connect_args={'check_same_thread': False})
else:
    engine = create_engine(MYSQL_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()