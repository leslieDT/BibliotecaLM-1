from flask_restful import Resource, reqparse
from . import api, db
from .models import Book

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('author')
parser.add_argument('genre')
parser.add_argument('year', type=int)

class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return [{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'year': book.year} for book in books]

    def post(self):
        args = parser.parse_args()
        new_book = Book(title=args['title'], author=args['author'], genre=args['genre'], year=args['year'])
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added', 'book': {'id': new_book.id, 'title': new_book.title, 'author': new_book.author, 'genre': new_book.genre, 'year': new_book.year}}, 201

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'year': book.year}

    def put(self, book_id):
        args = parser.parse_args()
        book = Book.query.get_or_404(book_id)
        book.title = args['title']
        book.author = args['author']
        book.genre = args['genre']
        book.year = args['year']
        db.session.commit()
        return {'message': 'Book updated', 'book': {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'year': book.year}}

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted'}

api.add_resource(BookListResource, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')
