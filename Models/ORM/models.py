from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.model):
    __tablename__="books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, primary_key=True)
    reviews = db.relationship("Reviews", backref = "books")

class Users(db.model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String, nullable=False)
    password= db.Column(db.String, nullable=False)
    reviews = db.relationship("Reviews", backref = "users")

class Reviews(db.model):
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
