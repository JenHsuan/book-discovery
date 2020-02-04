def initial_session(session):
    if session.get("user") is None:
        session["user"] = "empty"

def is_session_empty(session):
    if session['user'] == "empty":
        return True
    else:
        return False

def set_session(session, value):
    session["user"] = value

def get_session(session):
    return session["user"]

def reset_session(session):
    session["user"] = "empty"

def get_user_id(db, name):
    res = db.execute("select id from users where username = :name",
              {"name": name}).first()
    if res == None:
        return None
    
    return res