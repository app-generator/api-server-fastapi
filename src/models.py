from src.helpers.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(40), nullable=False, )
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(40), nullable=False)

class JWTTokenBlocklist(Base):
    __tablename__ = 'blocked_jwt'
    
    id = Column(Integer, primary_key=True, nullable=False)
    jwt_token = Column(String(40), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))


# create a table that will store blocked jwt tokens
# whenever a request comes in that looks at the jwt token, 



# when the 