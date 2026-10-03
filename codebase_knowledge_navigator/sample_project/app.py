from database import get_user
from auth import authenticate

def login(username, password):
    if authenticate(username, password):
        return get_user(username)
    return None
