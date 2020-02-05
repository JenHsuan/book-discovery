import os
import json

from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from flask_session import Session
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from Utils.register import checkForRestration, createNewAccount
from Utils.review import createNewReview, get_reviews
from Utils.book import getBook, getFirstBookByTitle, getFirstBookByAuthor, getFirstBookByIsbn, initial_book_session, is_book_session_empty, set_book_session, get_book_session, reset_book_session
from Utils.login import checkForLogin
from Utils.user import initial_session, is_session_empty, set_session, get_session, reset_session, get_user_id

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods = ["GET"])
def cover():
    return render_template("cover.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        initial_session(session)

        if is_session_empty(session):
            return render_template("login.html")
        else:
            return redirect(url_for('search'))

    else:
        #after the user submits the form
        name = request.form.get("name")
        password = request.form.get("password")
        res = checkForLogin(db, name, password)
        if res != False:
            return render_template("login.html", errorMsg=res)

        set_session(session, name)
        return redirect(url_for('search'))

@app.route("/search", methods = ["GET", "POST"])
def search():
    if request.method == "GET":
        user = get_session(session)
        if user is None or user == 'empty':
            return render_template("login.html")
        else:
            return render_template("search.html", username=session['user'])
    else:
        search_param = request.form.get("search_param")
        search_keyword = request.form.get("search_keyword")
        res = ""
        res = getBook(db, search_param, search_keyword)
        reviews = get_reviews(db, res["id"])
        initial_book_session(session)
        set_book_session(session, res["id"])
        return render_template("search_result.html", search_result = res, reviews = reviews)

    
@app.route("/logout", methods = ["GET"])
def logout():
    reset_session(session)
    reset_book_session(session)
    return render_template("login.html")

@app.route("/review", methods = ["POST"])
def review():
    #book_id, user_id, grade, review_comment
    grade = int(request.form.get("grade"))
    comment = request.form.get("comment")
    book_id = get_book_session(session)
    user_id = get_user_id(db, session["user"])["id"]

    res = createNewReview(db, book_id, user_id, grade, comment)
    if res == False:
        return render_template("search.html", username=session['user'])
    else:
        return render_template("search.html", username=session['user'], errorMsg = res)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("name")
        password = request.form.get("password")
        res = checkForRestration(db, username, password)
        if res != False:
            return render_template("register.html", errorMsg=res)
    
        createNewAccount(db, username, password)
        set_session(session, username)
        return redirect(url_for('search'))

@app.route("/api/<isbn>", methods = ["GET"])
def getBooByIsbn(isbn):
    #Get books by isbn from the database
    return jsonify(getFirstBookByIsbn(db, isbn)), 200
db
@app.route("/api/title/<title>", methods = ["GET"])
def getBookByTitle(title):
    #Get books by title from the database
    return jsonify(getFirstBookByTitle(db, title)), 200

@app.route("/api/author/<author>", methods = ["GET"])
def getBookByAuthor(title):
    #Get books by title from the database
    return jsonify(getFirstBookByTitle(bn, title)), 200

if __name__ == '__main__':
    app.run()