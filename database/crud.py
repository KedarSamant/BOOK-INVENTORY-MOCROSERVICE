from sqlalchemy.orm import Session
from . import models, schemas

from fastapi import HTTPException

# Function to create and return the Book
def create_book(db: Session, book: schemas.BookCreate):

    
    book_data = book.dict(exclude_unset=True)

    # Handle genre creation if needed
    if book_data.get('genre_name'):
        genre = db.query(models.Genre).filter(
            models.Genre.name.ilike(book_data['genre_name'])
        ).first()

        if not genre:
            genre = models.Genre(name=book_data['genre_name'])
            db.add(genre)
            db.commit()
            db.refresh(genre)

        book_data['genre_id'] = genre.id

    book_data.pop('genre_name', None)

    # Create the book in the database
    db_book = models.Book(**book_data)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    # Make sure `copies_sold` is available
    copies_sold = db_book.copies_sold if db_book.copies_sold else 0

    # Return the response using BookResponse schema
    return schemas.BookResponse(
        id=db_book.id,
        title=db_book.title,
        author=db_book.author,
        isbn=db_book.isbn,
        published_date=db_book.published_date,
        price=db_book.price,
        genre_id=db_book.genre_id,
        genre_name=db_book.genre.name if db_book.genre else None,
        copies_sold=copies_sold,  
    )

def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for key, value in book.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        
        db.commit()
        db.refresh(db_book)
        
        # Calculate total_revenue after update
        db_book.total_revenue = db_book.copies_sold * db_book.price
        
        return db_book
    return None



def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None

def sell_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        if db_book.copies_available <= 0:
            return None
        db_book.copies_available -= 1
        db_book.copies_sold += 1
        db.commit()
        db.refresh(db_book)
    return db_book


def search_books(db: Session, author: str = None, title: str = None, 
                 min_price: float = None, max_price: float = None,
                 genre_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Book)
    
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if min_price is not None:
        query = query.filter(models.Book.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Book.price <= max_price)
    if genre_id is not None:
        query = query.filter(models.Book.genre_id == genre_id)
        
    return query.offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        # Calculate total_revenue dynamically
        total_revenue = db_book.copies_sold * db_book.price
        db_book.total_revenue = total_revenue  # Add to the object
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10):
    db_books = db.query(models.Book).offset(skip).limit(limit).all()
    for book in db_books:
        book.total_revenue = book.copies_sold * book.price  # Calculate total revenue dynamically
    return db_books


def get_total_revenue(db: Session):
    total = 0.0
    books = db.query(models.Book).all()
    for book in books:
        total += book.copies_sold * book.price
    return {"total_revenue": total}