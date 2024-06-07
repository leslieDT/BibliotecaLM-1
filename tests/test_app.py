import unittest
from app import create_app, db
from app.models import Book

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        response = self.client.post('/api/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'year': 2024
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Book', response.json['book']['title'])

    def test_get_books(self):
        self.client.post('/api/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'year': 2024
        })
        response = self.client.get('/api/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_book(self):
        self.client.post('/api/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'year': 2024
        })
        response = self.client.put('/api/books/1', json={
            'title': 'Updated Book'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Book', response.json['book']['title'])

    def test_delete_book(self):
        self.client.post('/api/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'year': 2024
        })
        response = self.client.delete('/api/books/1')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/books')
        self.assertEqual(len(response.json), 0)

if __name__ == '__main__':
    unittest.main()