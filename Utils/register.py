from flask import jsonify
from Utils.encript import hash_password

def checkForRestration(db, username, password):
    if username == None:
        return "The username shouldn't be empty"
    
    if password == None:
        return "The password shouldn't be empty"

    res = db.execute("select * from users where username = :username",
              {"username": username}).first()

    if res != None:
        return "The username is already exist"
    
    return False

def createNewAccount(db, username, password):
    hashed_password = hash_password(password)
    db.execute("insert into users (username, password) values (:username, :password)", 
                    {"username": username, "password": hashed_password})
    db.commit()