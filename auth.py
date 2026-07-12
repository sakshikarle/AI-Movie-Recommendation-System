from werkzeug.security import generate_password_hash, check_password_hash
from database.mongodb import users

def register_user(username, email, password):

    existing_user = users.find_one({
        "$or": [
            {"username": username},
            {"email": email}
        ]
    })

    if existing_user:
        return False

    users.insert_one({
        "username": username,
        "email": email,
        "password": generate_password_hash(password)
    })

    return True


def login_user(username, password):

    user = users.find_one({"username": username})

    if user and check_password_hash(user["password"], password):
        return user

    return None