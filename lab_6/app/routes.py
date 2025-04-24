from flask import Blueprint, abort, request
from flask_restful import Resource
from marshmallow import ValidationError
from .models import BookShema, Book
from app import db

book_schema = BookShema()

main = Blueprint("lab_6", __name__)

class BookListResource(Resource):
    def get(self):
        last_id = request.args.get("last_id", 0, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        books = Book.query.filter(Book.id > last_id).order_by(Book.id).limit(per_page).all()
        books_list=[{"id": book.id, "title":book.title, "author":book.author} for book in books]
        next_id = books[-1].id if books else None
        return {
            "books": books_list,
            "next_id": next_id
        }, 200
    
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Empty request"}, 400 
        try:
            validated_data = book_schema.load(data)

            new_book = Book(
                            title=validated_data["title"], 
                            author=validated_data["author"]
                            )

            db.session.add(new_book)
            db.session.commit()
            return {
                    "message": "Book created successfully", 
                    "book": {"id": new_book.id, "title": new_book.title, "author": new_book.author}
                }, 201
        except ValidationError as e:
            return {"error": e.errors()}, 400

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        book_json = [{"id": book.id, "title":book.title, "author":book.author}]
        if book is not None:
            return book_json ,200
        else:
            abort(404)

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message":"Book successful deleted"},200

@main.errorhandler(404)
def page_not_found(error):
    return {"error":"out of range"},404

    