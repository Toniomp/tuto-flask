import click
from .app import app, db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    print(filename)
    db.create_all()

    import yaml
    books = yaml.load(open(filename),Loader=yaml.Loader)

    from .models import Author, Book

    authors = {}
    for b in books:
        a = b["author"]
        if a not in authors:
            o = Author(name = a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()

    for b in books:
        a = authors [b["author"]]
        o = Book(price = b["price"],
            title = b["title"],
            url = b["url"],
            image = b["img"],
            author_id = a.id)
        db.session.add(o)
    db.session.commit()
    
@app.cli.command()
def syncdb ():
    """Creates all missing tables. """
    db.create_all()
    
@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username:str, password:str):
    '''add a new user'''
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username=username, password=m.hexdigest())
    db.session.add(u)
    db.session.commit()

@app.cli.command()
@click.argument('username')
#@click.argument('old_passwd')
@click.argument('new_passwd')
def passwd(username:str, new_passwd:str):
    '''change user password'''
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(new_passwd.encode())
    user = User.query.get(username)
    user = User(username=username, password=new_passwd.hexdigest())
    db.session.commit()


@app.cli.command()
@click.argument('genre_name')
def add_genre(genre_name: str): # mettre un tiret du 6 lors de l'appel de la commande
    '''ajoute un nouveau genre dans la table Genre'''
    from .models import Genre
    genre = Genre(name=genre_name)
    db.session.add(genre)
    db.session.commit()

@app.cli.command()
@click.argument('book_id')
@click.argument('genre_name')
def add_genre_to_book(book_id: int, genre_name: str):
    '''ajoute un genre à un livre dans la base de données'''
    from .models import Book, Genre, db
    
    book = Book.query.get(book_id)
    genre = Genre.query.filter_by(name=genre_name).first()
    if (book is not None) and genre :
        if genre not in book.genres:
            book.genres.append(genre)
            db.session.commit()
