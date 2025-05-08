from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
import os
from dotenv import load_dotenv

#loading envirnmentv variable from .env file
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')


#this engine creates connection of database with python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False}
                       )
#this sessionmaker creates a session of database
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

class Base(DeclarativeBase):
    pass








