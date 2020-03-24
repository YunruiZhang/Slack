# user is a list of dictionarys contain user info. there are uid, email, password in the dictioary
# tokens is a list of token which is valid
# channels is a list of dicts contain existing channels info.
# msgs is a list of dicts contain msg infos including the channel id which the msg in 
# and the sender of it , the time it sent and the msg itself.

DATABASE = {
    'users' : [],
    'tokens' : [],#make this a feature of users maybe ?
    'channels' : [],
    'messages' : [],
}

SECRET = 'thesecret'

def getData():
    global DATABASE
    return DATABASE


def token_generate():
    pass

def create_user(email, password, name_first, name_last):
    DATA = getData
    
    new_user = {
        'name_first': name_first, 
        'name_last': name_last, 
        'password': password, 
        'email': email,
        # ect.
    }
    
    DATA['users'].append(new_user)
    return {}
    

def create_channel():
    pass

def create_message():
    pass