import channel
import channels
import auth
import pytest
import database
from error import InputError, AccessError
import json
import urllib
import flask 
import message

BASE_URL = 'http://127.0.0.1:8081'

def test_message_send():
    u_id, token = get_user("user1")
    channel = channels.channels_create(token, "channel1", True)
    channel_id = int(channel['channel_id'])
    data = json.dumps({
        'token': token,
        'channel_id': channel_id,
        'message': 'test',
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    data = database,getData()
    assert int(payload['message_id']) == int(data['message'][0]['message_id'])
"""def test_message_send_except():
    urllib.request.urlopen(f"{BASE_URL}/message/send")
    u_id, token = get_user("user1")
    channel_id1 = channels.channels_create(token, "channel1", True)
    data = json.dumps{[
        'token': token,
        'channel_id': channel_id1,
        'message': 'a'*1001,
    ]}.encode('utf-8')

    with pytest.raises(InputError) as e:
		urllib.request.Request(f"{BASE_URL}/message/send", data=data, headers={'Content-Type': 'application/json'})"""










def get_user(username):

   #auth.auth_register(username+"@email.com", username+"pass", "John", "Doe")
    
    # Can use this otherwise
    #return auth.auth_login("example@email.com","password")

    # Use this if auth functions aren't implemented
    DATA = database.getData()

    DATA['users'].append( {'u_id' : int(username[-1]),
            'name_first': "example first", 
            'name_last': "example last", 
            'password': "badpassword", 
            'handle_str': 'hayden',
            'email': "email@example.com"
            })

    return(int(username[-1]), database.token_generate(int(username[-1])))



