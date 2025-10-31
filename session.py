# session.py
current_user_id = None

def set_user_id(user_id):
    global current_user_id
    current_user_id = user_id

def get_user_id():
    return current_user_id
