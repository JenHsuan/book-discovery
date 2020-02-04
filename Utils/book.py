import os
import requests
from flask import jsonify

def getBook(db, type, keyword):
    if type == "title":
        res = getFirstBookByTitle(db, keyword)
    elif type == "author":
        res = getFirstBookByAuthor(db, keyword)
    else:
        res = getFirstBookByIsbn(db, keyword)

    return res
            
def getFirstBookByTitle(db, title):
    book = db.execute("select id, title, author, year, isbn from books where title like :title",
              {"title": "%" + str(title) + '%'}).first()
    if book == None:
        return {}

    dic = dict(book)
    updateStastic(db, book["id"], dic)
    return dic

def getFirstBookByIsbn(db, isbn):
    book = db.execute("select id, title, author, year, isbn from books where isbn like :isbn",
              {"isbn": str(isbn) + '%'}).first()
    if book == None:
        return {}

    dic = dict(book)
    updateStastic(db, book["id"], dic)
    return dic

def getFirstBookByAuthor(db, author):
    book = db.execute("select id, title, author, year, isbn from books where author like :author",
              {"author": "%" + str(author) + '%'}).first()
    if book == None:
        return {}

    dic = dict(book)
    updateStastic(db, book["id"], dic)
    return dic

def updateStastic(db, book_id, dic):
    isbn = db.execute("select isbn from books where id = :book_id",
              {"book_id": book_id}).first()

    res = requests.get("https://www.goodreads.com/book/review_counts.json",
        params = {"key": os.getenv("GOODREADS_KEY"), "isbns": isbn})
    
    if res.status_code == 404:
        dic.update( {'average_score' : 0} )       
        dic.update( {'review_count' : 0} ) 
    else:
        dic.update( {'average_score' : res.json()["books"][0]["average_rating"]} )       
        dic.update( {'review_count' : res.json()["books"][0]["work_ratings_count"]} ) 

def initial_book_session(session):
    if session.get("book_id") is None:
        session["book_id"] = "empty"

def is_book_session_empty(session):
    if session["book_id"] == "empty":
        return True
    else:
        return False

def set_book_session(session, value):
    session["book_id"] = value

def get_book_session(session):
    return session["book_id"]

def reset_book_session(session):
    session["book_id"] = "empty"