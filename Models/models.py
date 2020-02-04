class Book:
    def __init__(self, id, isbn, title, author, year):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        #self.reviews = []

    #def add_review(self, review):
        #review.book_id = self.id
        #self.reviews.append(review)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class Review:
    def __init__(self, id, user_id, book_id, average_score, review_comment, review_count):
        self.id = id
        self.user_id = user_id
        self.book_id = book_id
        self.average_score = average_score
        self.review_comment = review_comment
        self.review_count = review_count
