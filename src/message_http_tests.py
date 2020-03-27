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

BASE_URL = 'http://127.0.0.1:8080'

def test_message_send():
    urllib.request.urlopen(f"{BASE_URL}/message/send")
    u_id, token = get_user("user1")
    channel_id1 = channels.channels_create(token, "channel1", True)
    data = json.dumps{[
        'token': token,
        'channel_id': channel_id1,
        'message': 'test',
    ]}.encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", data=data, headers={'Content-Type': 'application/json'})
    assert 
def test_message_send_except():
    urllib.request.urlopen(f"{BASE_URL}/message/send")
    u_id, token = get_user("user1")
    channel_id1 = channels.channels_create(token, "channel1", True)
    data = json.dumps{[
        'token': token,
        'channel_id': channel_id1,
        'message': 'a'*1001,
    ]}.encode('utf-8')

    with pytest.raises(InputError) as e:
		urllib.request.Request(f"{BASE_URL}/message/send", data=data, headers={'Content-Type': 'application/json'})










def get_user(username):
    auth.auth_register(username+"@email.com", username+"pass", "John", "Doe")
    return auth.auth_login("example@email.com","password")
def get_channel()