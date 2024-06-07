# app/models.py

from . import db  # Importa el objeto db de tu aplicación
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200))  # URL de la imagen del libro


    def __repr__(self):
        return f'<Book {self.title}>'