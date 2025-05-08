from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date
from typing import Optional
import re

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    published_date: date
    price: float
    genre_id: int
    copies_available: Optional[int] = 1

class BookCreate(BookBase):
    @field_validator('title', 'author')
    @classmethod
    def check_empty_string(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()
    
    @field_validator('isbn')
    @classmethod
    def check_isbn(cls, v: str) -> str:
        isbn10_regex = r'^(?:\d[\ |-]?){9}[\d|X]$'
        isbn13_regex = r'^(?:\d[\ |-]?){13}$'
        
        if not (re.fullmatch(isbn10_regex, v) or re.fullmatch(isbn13_regex, v)):
            raise ValueError("Invalid ISBN format")
        return v
    
    @field_validator('published_date')
    @classmethod
    def check_date_not_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Published date cannot be in the future")
        return v
    
    @field_validator('price')
    @classmethod
    def check_positive_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Price must be positive")
        return v

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int
    copies_sold: int
    total_revenue: float
    
    model_config = ConfigDict(from_attributes=True)  # Replaces orm_mode

class Genre(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)