from fastapi import FastAPI
from pydantic import BaseModel
from bson import ObjectId
from pymongo import MongoClient
from fastapi.responses import JSONResponse
import os
from mongo_client import get_db

db = get_db()
books_col = db["books"]


app = FastAPI()

# --- Root Route ---
@app.get("/")
def root():
    return {"message": "✅ FastAPI Library API is running on Vercel!"}

# --- MongoDB Connection ---
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Use default values for testing (optional, remove in production)
if not MONGO_URI or not DB_NAME:
    print("⚠️ MongoDB environment variables not found. Running in mock mode.")
    books_col = None
else:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    books_col = db["books"]

# --- Helper ---
def serialize_book(book):
    book["_id"] = str(book["_id"])
    return book

# --- Models ---
class Book(BaseModel):
    title: str
    author: str
    genre: str
    copies: int

# --- Routes ---
@app.get("/books")
def get_books():
    if books_col is None:
        return JSONResponse(content={"error": "MongoDB not configured"}, status_code=500)
    books = list(books_col.find())
    return [serialize_book(b) for b in books]

@app.post("/books")
def add_book(book: Book):
    if books_col is None:
        return JSONResponse(content={"error": "MongoDB not configured"}, status_code=500)
    books_col.insert_one(book.dict())
    return {"message": "Book added successfully"}

@app.delete("/books/{book_id}")
def delete_book(book_id: str):
    if books_col is None:
        return JSONResponse(content={"error": "MongoDB not configured"}, status_code=500)
    books_col.delete_one({"_id": ObjectId(book_id)})
    return {"message": "Book deleted successfully"}
