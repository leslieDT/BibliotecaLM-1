import os

class Config:
    # Utiliza una clave secreta fuerte para la seguridad de la aplicación
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Especifica la ruta de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///biblioteca.db'

    # Deshabilita el seguimiento de modificaciones para evitar advertencias
    SQLALCHEMY_TRACK_MODIFICATIONS = False
