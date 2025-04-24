from pydantic import BaseModel, Field

def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
    }

class BookCreate(BaseModel):
    title: str = Field(..., min_length=5)
    author: str = Field(..., min_length=5)

class Book(BookCreate):
    id: str