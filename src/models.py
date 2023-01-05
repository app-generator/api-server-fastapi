from src.helpers.database import Base
from sqlalchemy import Column, String, Integer

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(40), nullable=False, )
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(40), nullable=False)



# create a table that will store blocked jwt tokens
# whenever a request comes in that looks at the jwt token, 



# when the 