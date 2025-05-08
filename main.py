from fastapi import FastAPI
from database import models, session

app = FastAPI(title="Book Inventory API")

models.Base.metadata.create_all(bind=session.engine)


@app.get("/")
def book_inventory():
    return {"status": "lets go!"}