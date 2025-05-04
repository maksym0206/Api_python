from fastapi import APIRouter, Request
from marshmallow import ValidationError
from .models import Book


books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
]

book_schema = Book()
main = APIRouter()


@main.get("/")
async def get_books():
    return {"books": books}

@main.get("/{book_id}")
async def get_books(book_id: int):
    book = find_book_by_id(book_id)
    if book is not None:
        return {"book": book}
    else:
        return {"message": "Out of range"}
    

@main.post("/create_book/")
async def create_book(request: Request):
    data = await request.json()
    if not data:
        return {"error": "Empty request"}, 400
    try:
        validated_data = book_schema.load(data)
        new_id = max(book["id"] for book in books) + 1 if books else 1
        validated_data["id"] = new_id
        books.append(validated_data)
        return (validated_data)
    except ValidationError as e:
        return {"error": e.errors()},400

@main.delete("/{book_id}/delet_book")
async def delet_book(book_id: int):
    global books
    book = find_book_by_id(book_id)
    if book is None:
        return {"message": f"Book {book_id} not found"}
    books = [b for b in books if b["id"] != book_id]
    return {"message": f"Book {book_id} successfully deleted"}

def find_book_by_id(book_id: int):
    return next((book for book in books if book["id"] == book_id), None)

    