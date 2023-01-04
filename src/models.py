from src.helpers.database import Base
from sqlalchemy import Column, String, Integer

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(40), nullable=False, )
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(40), nullable=False)