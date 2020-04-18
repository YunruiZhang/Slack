# user is a list of dictionarys contain user info. there are uid, email, password in the dictioary
# tokens is a list of token which is valid
# channels is a list of dicts contain existing channels info.
# msgs is a list of dicts contain msg infos including the channel id which the msg in
# and the sender of it , the time it sent and the msg itself.
from datetime import datetime
import json
import os
import shutil
import jwt
from error import InputError, AccessError
BASE_URL = 'http://127.0.0.1:8081'

'''
EXAMPLE OF HOW THE CHANNELS DATABASE STRUCTURE LOOKS:

"channels" : [
        {
            "channel_id":1,
            "public":1,
            "details" : {
            "name": "example name",
            "owner_members": [
                {
                    "u_id": 1,
                    "name_first": "example first",
                    "name_last": "example last",
                }
            ],
            "all_members": [
                {
                    "u_id": 1,
                    "name_first": "example first",
                    "name_last": "example last",
                }
            ],
            },
            "messages":[{"ADD THE MESSAGE DICTIONARY TO THIS LIST PLEASE"}]
        }
    ]
'''

DATABASE = {
    'users' : [],
    'channels' : [],
    'messages' : []
}

SECRET = 'thesecret'

def getData():
    #global DATABASE
    a_file = open("database.json", "r")
    DATABASE_TO_RETURN = json.load(a_file)
    a_file.close()

    return DATABASE_TO_RETURN

def token_generate(u_id):
    '''

    {
        "alg": "HS256",
        "typ": "JWT"
    }
    {
        "u_id": "u_id"
    }
    {
        SECRET
    }
    '''
    encoded_jwt = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
    return encoded_jwt.decode("utf-8")

def verify_token(token):
    # IF THE TOKEN IS VALID THEN IT RETURNS THE U_ID OTHERWISE IT RETURNS FALSE
    token.encode('utf-8')
    try:
        decoded_jwt = jwt.decode(token, SECRET, algorithms=['HS256'])
    except:
        return False

    return decoded_jwt['u_id']

######################message code##############################
def new_message(message_id, channel_id, user_id, message):
    DATA = getData()
    time = datetime.now()
    new_message_to_send = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time.timestamp(),
        'reacts': [{
            #Only likes for now (ID 1)
            'react_id': 1,
            'u_ids': []
        }],
        'is_pinned': False
    }
    short_msg = {
        'message_id': message_id,
        'channel_id': int(channel_id)
    }
    DATA['messages'].append(short_msg)
    #print(DATABASE['messages'])
    for i in DATA['channels']:
        if int(i['channel_id']) == int(channel_id):
            #print('hello')
            i['messages'].append(new_message_to_send)
            #print(i['messages'])
            break
    update_database(DATA)
    return {}
##########################################################
def create_user(u_id, permission_id, handle, token, email, password, name_first, name_last):

    DATA = getData()

    new_user = {
        'u_id': u_id,
        'permission_id': permission_id,
        'handle_str': handle,
        'token': token,
        'name_first': name_first,
        'name_last': name_last,
        'password': password,
        'email': email,
        'profile_img_url':""
    }
    DATA['users'].append(new_user)
    update_database(DATA)
    return {}

def reset_db():
    DATA = {
        'users' : [],
        'channels' : [],
        'messages' : []
    }
    root_dir = os.path.dirname(os.getcwd())
    folder = os.path.join(root_dir, 'src/static')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

        update_database(DATA)

    return {}

def update_database(DATA):
    #print(DATA)
    a_file = open("database.json", "w")
    json.dump(DATA, a_file)
    a_file.close()
    return {}

def change_permission(token, u_id, permission_id):
    DATA = getData()

    if permission_id != 1 and permission_id != 2:
        raise InputError("Invalid permission ID")

    owner_flag = False
    user_to_change = None

    for users in DATA['users']:
        if users['u_id'] == u_id:
            user_to_change = users
        if users['u_id'] == verify_token(token):
            if users['permission_id'] == 1:
                owner_flag = True

    if not owner_flag:
        raise AccessError("Authorised user not an owner")

    user_to_change['permission_id'] = permission_id
    update_database(DATA)
    return {}

def remove_users(token, u_id):
    DATA = getData()

    owner_flag = False
    user_to_change = None

    for users in DATA['users']:
        if users['u_id'] == u_id:
            user_to_change = users
        if users['u_id'] == verify_token(token):
            if users['permission_id'] == 1:
                owner_flag = True

    if not owner_flag:
        raise AccessError("Authorised user not an owner")

    if not user_to_change:
        raise InputError("User ID does not refer to valid user")

    DATA['users'].remove(user_to_change)
    update_database(DATA)
    return {}
