from fastapi import APIRouter, HTTPException, Request
from app.models import Book, book_helper, BookCreate
from app.database import book_collection
from bson import ObjectId
from bson.errors import InvalidId

main = APIRouter()


@main.get("/")
async def get_books():
    books = []
    async for book in book_collection.find():
        books.append(book_helper(book))
    return {"books": books}

@main.get("/{book_id}")
async def get_books(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    book = await book_collection.find_one({"_id": obj_id})
    if book:
        return book_helper(book)
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    
@main.post("/create_book")
async def create_book(book: BookCreate):
    new_book = book.model_dump()
    result = await book_collection.insert_one(new_book)
    created_book = await book_collection.find_one({"_id": result.inserted_id})
    return book_helper(created_book)

@main.delete("/{book_id}/delete_book")
async def delet_book(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    result = await book_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 1:
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")



    