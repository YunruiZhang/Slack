# user is a list of dictionarys contain user info. there are uid, email, password in the dictioary
# tokens is a list of token which is valid
# channels is a list of dicts contain existing channels info.
# msgs is a list of dicts contain msg infos including the channel id which the msg in 
# and the sender of it , the time it sent and the msg itself.

DATABASE = {
    user = []
    tokens = []
    channels = []
    msgs = []
}

SECRET = 'thesecret'

def getData():
    global DATABASE
    return DATABASE






