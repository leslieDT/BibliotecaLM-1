from flask import Blueprint, render_template, request, redirect, url_for
from .models import Book, db
from flask_restful import Resource, reqparse
from .models import Book, db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@main.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        new_book = Book(title=title, author=author, genre=genre, year=year)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_book.html')

@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.year = request.form['year']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update_book.html', book=book)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.index'))



class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return [{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'year': book.year} for book in books]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('author', required=True)
        parser.add_argument('genre', required=True)
        parser.add_argument('year', required=True, type=int)
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
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('author')
        parser.add_argument('genre')
        parser.add_argument('year', type=int)
        args = parser.parse_args()
        book = Book.query.get_or_404(book_id)
        if args['title']:
            book.title = args['title']
        if args['author']:
            book.author = args['author']
        if args['genre']:
            book.genre = args['genre']
        if args['year']:
            book.year = args['year']
        db.session.commit()
        return {'message': 'Book updated', 'book': {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'year': book.year}}

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted'}

from flask import request

@main.route('/search')
def search():
    query = request.args.get('query')
    # Realizar la búsqueda en la base de datos según el query
    # books = Book.query.filter(...).all() 
    return render_template('search_results.html', books=books, query=query)