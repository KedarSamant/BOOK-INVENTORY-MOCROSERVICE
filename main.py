from fastapi import FastAPI
from database import models, session
from routers import books  # Import your router module

app = FastAPI(
    title="Book Inventory API",
    description="API for managing book inventory",
    version="1.0.0"
)

# Create database tables on startup
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=session.engine)

# Include all routes from the books router
app.include_router(books.router, prefix="/api/books")

# Root route
@app.get("/")
def book_inventory():
    return {"status": "Welcome to Book Inventory API!"}
