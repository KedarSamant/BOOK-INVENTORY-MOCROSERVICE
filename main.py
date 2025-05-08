#https://github.com/KedarSamant/BOOK-INVENTORY-MOCROSERVICE.git
from fastapi import FastAPI
from database import models, session
from routers import books
app = FastAPI(title="Book Inventory API")

models.Base.metadata.create_all(bind=session.engine)

app.include_router(books.router, prefix="/api/books")

#this is default route
@app.get("/")
def book_inventory():
    return {"status": "lets go!"}

