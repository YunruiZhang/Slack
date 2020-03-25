# user is a list of dictionarys contain user info. there are uid, email, password in the dictioary
# tokens is a list of token which is valid
# channels is a list of dicts contain existing channels info.   
# msgs is a list of dicts contain msg infos including the channel id which the msg in 
# and the sender of it , the time it sent and the msg itself.
import jwt

'''
EXAMPLE OF HOW THE CHANNELS DATABASE STRUCTURE LOOKS:

'users' : [ {'u_id' : 1,
            'name_first': "example first", 
            'name_last': "example last", 
            'password': "badpassword", 
            'handle_str': 'hayden',
            'email': "email@example.com"
            }, {
            'u_id': 2,
            'email': 'cs15few31@cse.unsw.edu.au',
            'name_first': 'Chris',
            'name_last': 'Chung',
            'handle_str': 'cchung',
            'password':"baddpass"
        }
        ],
    'tokens' : [],#make this a feature of users maybe ?
    'channels' : [
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
                },
                {
                    "u_id": 2,
                    "name_first": "get rid first",
                    "name_last": "get rid last",
                }
            ],
            },
            "messages":[{
                "message_id": 1,
                "u_id": 1,
                "message": "Hello world",
                "time_created": 1582426789,
                },{
                "message_id": 2,
                "u_id": 1,
                "message": "Hello there",
                "time_created": 1582426790,
            }]
        },
        {
            "channel_id":2,
            "public":1,
            "details" : {
            "name": "example name",
            "owner_members": [
                {
                    "u_id": 2,
                    "name_first": "example first",
                    "name_last": "example last",
                }
            ],
            "all_members": [
                {
                    "u_id": 2,
                    "name_first": "get rid first",
                    "name_last": "get rid last",
                }
            ],
            },
            "messages":[{
                "message_id": 1,
                "u_id": 1,
                "message": "Hello world",
                "time_created": 1582426789,
                },{
                "message_id": 2,
                "u_id": 1,
                "message": "Hello there",
                "time_created": 1582426790,
            }]
        }
    ],
    'messages' : [],
'''

DATABASE = {
    'users' : [],
    'channels' : [],
    'messages' : []
}

SECRET = 'thesecret'

def getData():
    global DATABASE
    return DATABASE


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


def create_user(email, password, name_first, name_last):
    DATA = getData
    
    new_user = {
        'u_id' : len(getData)+1,
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