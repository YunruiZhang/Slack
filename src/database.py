# user is a list of dictionarys contain user info. there are uid, email, password in the dictioary
# tokens is a list of token which is valid
# channels is a list of dicts contain existing channels info.
# msgs is a list of dicts contain msg infos including the channel id which the msg in 
# and the sender of it , the time it sent and the msg itself.
import jwt


DATABASE = {
    'users' : [], 
    'channels' : [],
    'messages' : [],
}

SECRET = 'thesecret'
"""user = {
    'name_first': name_first, 
    'name_last': name_last, 
    'password': password, 
    'email': email,
    'token': token,
    # ect.
    }
message = {
    'message_id': message_id,
    'channel_id': channel_id,
    'sender_id': user_id
    'data': data
}
channel = {
    'channel_id': channel_id,
    'creater': user_id,
    'member': []
    'messages':[]

}"""
def getData():
    global DATABASE
    return DATABASE

def getNewUser():
    user = {
    'name_first': name_first, 
    'name_last': name_last, 
    'password': password, 
    'email': email,
    'token': token,
    }
    return user
def token_verify(token):
    pass

def check_email(email):
    pass

def create_user(email, password, name_first, name_last):
    DATA = getData

def verify_channel(channel_id):
    pass

def verify_message(message_id):
    pass  
    

def new_message(message_id, channel_id, user_id, message ):
    global DATABASE
    new_message = {
        'message_id': message_id,
        'channel_id': channel_id,
        'sender_id': user_id
        'data': message
    }
    DATABASE['messages'].append(new_message)
    return True