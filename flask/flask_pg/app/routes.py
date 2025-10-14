from flask import Blueprint,request,jsonify
from . import db
from .models import Book

book_bp = Blueprint('api',__name__,url_prefix='/api/books')

@book_bp.get("/")
def get_books():
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books])

@book_bp.get("/<int:id>")
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

@book_bp.post('/')
def create_book():
    data = request.get_json()

    if not data or 'title' not in data or 'author' not in data or 'published_date' not in data:
        return jsonify({'error':'Please provide valid data'}),400
    
    new_book = Book(
        title = data['title'],
        author = data['author'],
        published_date = data['published_date']
    )

    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()),201

@book_bp.put('/<int:id>')
def update_book(id):
    existing_book = Book.query.get_or_404(id)
    data = request.get_json()

    if not data or 'title' not in data or 'author' not in data or 'published_date' not in data:
        return jsonify({'error':'Please provide valid data'}),400

    existing_book.title = data['title']
    existing_book.author = data['author']
    existing_book.published_date = data['published_date']
    
    db.session.commit()
    return jsonify(existing_book.to_dict())


@book_bp.delete("/<int:id>")
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify(),204