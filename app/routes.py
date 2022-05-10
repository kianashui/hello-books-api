from attr import validate
from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, abort, make_response, request


# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Title 1", "Description 1"),
#     Book(2, "Title 2", "Description 2"),
#     Book(3, "Title 3", "Description 3")
# ]

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        abort(make_response({"error": f"{book_id} is an invalid book ID"}, 400))
    
    book = Book.query.get(book_id)

    # for book in books:
    #     if book.id == book_id:
    #         return book
    if not book:
        abort(make_response({"error": f"book {book_id} not found"}, 404))
    return book

def validate_author(author_id):
    try:
        author_id = int(author_id)
    except ValueError:
        abort(make_response({"error": f"{author_id} is an invalid author ID"}, 400))
    
    author = Author.query.get(author_id)

    if not author:
        abort(make_response({"error": f"author {author_id} not found"}, 404))
    return author


# @books_bp.route("", methods=["GET"])
# def show_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })
#     return jsonify(books_response)

# @books_bp.route("/<book_id>", methods=["GET"])
# def show_requested_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }


@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"], description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)

    response_body = {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }

    return response_body

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated"))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()
    
    return make_response(jsonify(f"Book #{book.id} successfully deleted"))

@authors_bp.route("", methods=["GET"])
def read_all_authors():
    authors = Author.query.all()
    
    authors_response = []
    for author in authors:
        authors_response.append({
            "id": author.id,
            "name": author.name
        })
    return jsonify(authors_response)

@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book_by_specific_author(author_id):
    author = validate_author(author_id)
    request_body = request.get_json()

    new_book = Book(title=request_body["title"], description=request_body["description"], author_id=author_id)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_books_by_author(author_id):
    author = validate_author(author_id)
    books = Book.query.filter_by(author_id=author_id)
    response_body = []

    for book in books:
        response_body.append({
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "author": book.author.name
        })

    # alternative to the above:
    # author = validate_author(author_id)
    # response_body = []
    # for book in author.books:
    #     response_body.append({
    #         "id": book.id,
    #         "title": book.title,
    #         "description": book.description,
    #         "author": book.author.name
    #     })
    # return jsonfiy(response_body)
    
    return make_response(jsonify(response_body), 200)
