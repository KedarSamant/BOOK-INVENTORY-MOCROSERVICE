#perform all CRUD operations
from sqlalchemy.orm import Session
from . import models, schemas

#getting single book from database
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

#getting all books from database
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

#create new book record in database  
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


#updating book record of perticular id in database
def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for key, value in book.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


#deleting book record of perticular id in database
def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
