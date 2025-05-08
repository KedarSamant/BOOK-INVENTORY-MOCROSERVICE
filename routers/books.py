#all routes for books 
from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session #it is tool for talk to databaese
from typing import List,Optional
from database import crud,schemas,session

router = APIRouter(tags=['books'])

def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()
   
#create new book record in database     
@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


#getting single book from database
@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


#updating book record of perticular id in database
@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id=book_id, book=book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


#deleting book record of perticular id in database
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    if not crud.delete_book(db, book_id=book_id):
        raise HTTPException(status_code=404, detail="Book not found")