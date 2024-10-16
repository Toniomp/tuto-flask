from .app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms.validators import DataRequired
from .app import login_manager


book_genre = db.Table('book_genre',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')))

user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.String(50), db.ForeignKey('user.username')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

class Author (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column (db.String(100))

    def __repr__ (self ):
        return "Author (%d) %s" % (self.id, self.name)
    
class User(db.Model, UserMixin ):
    username = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String(64))
    favorites = db.relationship('Book', secondary=user_favorites,
                                     backref=db.backref('favorited_by', lazy='dynamic'))

    def get_id (self):
        return self.username
    
    def add_to_favorites(self, book):
        if book not in self.favorites:
            self.favorites.append(book)

    def remove_from_favorites(self, book):
        if book in self.favorites:
            self.favorites.remove(book)
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Float)
    url = db.Column(db.String(500))
    image = db.Column(db.String(200))
    title = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author",
        backref = db.backref("books", lazy="dynamic"))
    genres = db.relationship('Genre', secondary=book_genre, lazy='subquery',
                             backref=db.backref('books', lazy=True))
    
    def __repr__ (self ):
            return "<Book (%d) %s>" % (self.id , self.title)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

def get_sample():
    return Book.query.limit(30).all()

def get_author(id):
    return  Author.query.get_or_404(id)  

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
