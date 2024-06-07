from flask import render_template, request, redirect, url_for, flash
from . import app, db
from .models import Book

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        
        new_book = Book(title=title, author=author, genre=genre, year=year)
        db.session.add(new_book)
        db.session.commit()
        
        flash('Book Added Successfully!')
        return redirect(url_for('index'))
    
    return render_template('add_book.html')

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.year = request.form['year']
        
        db.session.commit()
        
        flash('Book Updated Successfully!')
        return redirect(url_for('index'))
    
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    
    flash('Book Deleted Successfully!')
    return redirect(url_for('index'))
