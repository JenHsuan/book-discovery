from flask import jsonify

def createNewReview(db, book_id, user_id, grade, review_comment):
    if book_id == None or user_id == None:
        return "The book_id or the user_id shouldn't be empty"
    else:
        res = db.execute("select id from reviews where book_id = :book_id and user_id = :user_id",
          {"book_id": book_id, "user_id": user_id}).first()

        if res == None:
            user = db.execute("select * from users where id = :user_id",
             {"user_id": user_id}).first()
            if user == None:
                return "The user is not exist"

            if review_comment == None:
                return "The review_comment shouldn't be empty"
       
            if grade == None:
                return "The grade shouldn't be empty"

            db.execute("insert into reviews (book_id, user_id, score, review_comment) values \
                    (:book_id, :user_id, :grade, :review_comment)", 
                    {"book_id": book_id, "user_id": user_id, "grade": grade, "review_comment": review_comment})
            db.commit()

            return False

        else: 
            return "The user has already commented on this book"

def get_reviews(db, book_id):
    res = db.execute("select r.score, r.review_comment, u.username from \
          reviews as r left outer join users as u on r.user_id = u.id where r.book_id = :book_id",
          {"book_id": book_id}).fetchall()

    return res
