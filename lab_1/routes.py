from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError
from .models import Book


books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
]

book_schema = Book()

main = Blueprint("lab_1", __name__)

@main.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), 200

@main.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id),None)
    if book is not None:
        return jsonify(book),200
    else:
        abort(404)

@main.route("/create_book", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request"}), 400 
    try:
        validated_data = book_schema.load(data)
        new_id = max(book["id"] for book in books) + 1 if books else 1
        validated_data["id"] = new_id
        books.append(validated_data)
        return jsonify(validated_data), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

@main.route("/delete_book/<int:book_id>", methods=["delete"])
def delete_book(book_id):
    global books
    book_exists = any(book["id"] == book_id for book in books)
    if not book_exists:
        return jsonify({"error": "Book not found"}), 404
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"massage":"Book successful deleted"}),200

@main.errorhandler(404)
def page_not_found(error):
    return jsonify({"error":"out of range"}),404
    