from flask import Blueprint, jsonify, abort, make_response

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Title 1", "Description 1"),
    Book(2, "Title 2", "Description 2"),
    Book(3, "Title 3", "Description 3")
]

books_bp = Blueprint("books", __name__, url_prefix="/books")

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        abort(make_response({"error": f"{book_id} is an invalid book ID"}, 400))
    
    for book in books:
        if book.id == book_id:
            return book
    abort(make_response({"error": f"book {book_id} not found"}, 404)))


@books_bp.route("", methods=["GET"])
def show_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def show_requested_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }