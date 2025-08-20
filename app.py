# app.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__, template_folder='Templates', static_folder='Static')
CORS(app)

# DB config (use env vars or hardcode during dev)
DB_USER = os.environ.get('DB_USER', 'libuser')
DB_PASS = os.environ.get('DB_PASS', 'libpass')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'library_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    isbn = db.Column(db.String(64), unique=True)
    publisher = db.Column(db.String(255))
    year = db.Column(db.Integer)
    copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'year': self.year,
            'copies': self.copies,
            'available_copies': self.available_copies,
            'created_at': self.created_at.isoformat()
        }

# Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books-ui')
def books_ui():
    return render_template('books.html')

# API - CRUD
@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.order_by(Book.created_at.desc()).all()
    return jsonify([b.to_dict() for b in books])

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    b = Book.query.get_or_404(book_id)
    return jsonify(b.to_dict())

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'error': 'title required'}), 400

    # prevent duplicate ISBN
    isbn = data.get('isbn')
    if isbn and Book.query.filter_by(isbn=isbn).first():
        return jsonify({'error': 'ISBN already exists'}), 400

    book = Book(
        title=title,
        author=data.get('author'),
        isbn=isbn,
        publisher=data.get('publisher'),
        year=data.get('year'),
        copies=data.get('copies', 1),
        available_copies=data.get('available_copies', data.get('copies', 1))
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json() or {}
    for field in ['title','author','isbn','publisher','year','copies','available_copies']:
        if field in data:
            setattr(book, field, data[field])
    db.session.commit()
    return jsonify(book.to_dict())

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'deleted'})

# Search endpoint
@app.route('/api/search')
def search():
    q = (request.args.get('q') or '').strip()
    if not q:
        return jsonify([])
    pattern = f"%{q}%"
    books = Book.query.filter(
        or_(
            Book.title.ilike(pattern),
            Book.author.ilike(pattern),
            Book.isbn.ilike(pattern),
            Book.publisher.ilike(pattern)
        )
    ).all()
    return jsonify([b.to_dict() for b in books])

if __name__ == '__main__':
    # create tables if missing
    with app.app_context():
        db.create_all()
    app.run(debug=True)
