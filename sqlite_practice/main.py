import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create extension
db = SQLAlchemy()
# Create flask app
app = Flask(__name__)
# Create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialise app with extension
db.init_app(app)


# CREATE TABLE make sure to create it before app.create_all() or db won't recognize it
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


# Create all tables, will not provide migrations
with app.app_context():
    db.create_all()

# # CREATE RECORD
# with app.app_context():
#     new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()

# Select all items by title
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    print(all_books)

# Select single item
with app.app_context():
    book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    print(book)

# Get item by query
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.title == "Harry Potter"))
    book_to_update.title = "Harry Potter and the Chamber of Secrets"
    db.session.commit()

# Get item by primary key
with app.app_context():
    book_id = 1
    # scalar_one returns exception while scalar() returns None
    book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar_one()
    print(book_to_update)

# Delete item
with app.app_context():
    book_id = 1
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # or book_to_delete = db.get_or_404(Book, book_id)  
    db.session.delete(book_to_delete)
    db.session.commit()

# with app.app_context():
#     book_id = 1
#     book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
#     # or book_to_delete = db.get_or_404(Book, book_id)
#     db.session.delete(book_to_delete)
#     db.session.commit()


# cursor = db.cursor()
#
# # cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE,"
# #                " author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()
#


