from sqlalchemy import Column,Integer,Float,Date,String,ForeignKey
from sqlalchemy.orm import Relationship
from .session import Base

# creating genre table or model
# eack model must be derived from base in session.py

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,unique=True,index=True)
    books = Relationship('Book',back_populates='genre')
    
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    author = Column(String,nullable=False)
    isbn = Column(String,unique=True,nullable=False,index=True)
    published_date = Column(Date,nullable=False)
    price = Column(Float,nullable=False)
    copies_available = Column(Integer,default=1)
    copies_sold = Column(Integer,default=0)
    genre_id = Column(Integer,ForeignKey('genres.id'))
    genre = Relationship('Genre',back_populates='books')
    