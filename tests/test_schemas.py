from datetime import date
from database.schemas import BookCreate
from pydantic import ValidationError
import pytest

def test_valid_book_creation():
    # Test creating a book with valid data
    valid_book = BookCreate(
        title="Good Book",
        author="John Doe",
        isbn="978-3-16-148410-0",
        published_date=date(2020, 1, 1),
        price=10.99
    )
    assert valid_book.title == "Good Book"

def test_empty_title_fails():
    # Test that empty title fails validation
    with pytest.raises(ValidationError):
        BookCreate(
            title="",  # Empty title should fail
            author="Author",
            isbn="1234567890",
            published_date=date(2020, 1, 1),
            price=10.0
        )