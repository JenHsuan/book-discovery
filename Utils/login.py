from flask import jsonify
from Utils.encript import hash_password, verify_password

def checkForLogin(db, username, password):
    if username == None:
        return "The username shouldn't be empty"
    
    if password == None:
        return "The password shouldn't be empty"

    res = db.execute("select * from users where username = :username",
              {"username": username}).first()

    if res == None:
        return "The username doen't exist"
    
    if verify_password(res["password"], password) == False:
        return "Wrong password"
    
    return False

