import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db=scoped_session(sessionmaker(bind=engine))
#conn = engine.connect()
with open('books.csv', 'r', newline='') as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    for isbn, title, author, year in rows:
        db.execute("insert into books (isbn, title, author, year) values (:isbn, :title, :author, :year)", 
                   {"isbn": isbn, "title": title, "author": author, "year": year})
        
    db.commit()