from fastapi import FastAPI
from pydantic import BaseModel
from bson import ObjectId
from pymongo import MongoClient
import os

app = FastAPI()

# --- MongoDB Connection (Atlas via Environment Variables) ---
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI environment variable not found.")
if not DB_NAME:
    raise ValueError("❌ DB_NAME environment variable not found.")

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
@app.get("/")
def root():
    return {"message": "✅ FastAPI Library API is running!"}

@app.get("/books")
def get_books():
    books = list(books_col.find())
    return [serialize_book(b) for b in books]

@app.post("/books")
def add_book(book: Book):
    books_col.insert_one(book.dict())
    return {"message": "Book added successfully"}

@app.delete("/books/{book_id}")
def delete_book(book_id: str):
    books_col.delete_one({"_id": ObjectId(book_id)})
    return {"message": "Book deleted successfully"}
