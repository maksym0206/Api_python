from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError
from .models import BookShema, Book
from app import db

book_schema = BookShema()

main = Blueprint("lab_4", __name__)

@main.route("/books", methods=["GET"])
def get_books():
    last_id = request.args.get("last_id", 0, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    books = Book.query.filter(Book.id > last_id).order_by(Book.id).limit(per_page).all()
    books_list=[{"id": book.id, "title":book.title, "author":book.author} for book in books]
    next_id = books[-1].id if books else None
    return jsonify({
        "books": books_list,
        "next_id": next_id
    }), 200

@main.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    book_json = [{"id": book.id, "title":book.title, "author":book.author}]
    if book is not None:
        return jsonify(book_json),200
    else:
        abort(404)

@main.route("/create_book", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request"}), 400 
    try:
        validated_data = book_schema.load(data)
        new_book = Book(
                        title=validated_data["title"], 
                        author=validated_data["author"]
                        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book created successfully", "book": {"id": new_book.id, "title": new_book.title, "author": new_book.author}}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@main.route("/delete_book/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message":"Book successful deleted"}),200

@main.errorhandler(404)
def page_not_found(error):
    return jsonify({"error":"out of range"}),404
    