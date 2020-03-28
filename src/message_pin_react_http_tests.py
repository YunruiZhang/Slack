from urllib.request import urlopen, Request
from server import *
from json import loads, dumps
import pytest
from auth import * 
from error import InputError, AccessError
from database import getData
from channel_http_test import get_user


# set up
URL = 'http://127.0.0.1.8000'
D = getData()
# create a user
user = auth_register("")
# create a channel
create_channel_data = dumps({'token': token, 'name': 'channel_one', 'is_public': True, }).encode('utf-8')
channel_req = Request(URL+'/channels/create', data=create_channel_data, headers={'Content-Type':'application/json'})
channel_payload = urlopen(channel_req)
channel_id = int(channel_payload['channel_id'])
# send a message
send_message_data = dumps({'token': token, 'channel_id': channel_id, 'message': "FIRST_MESSAGE",}).encode('utf-8')
message_req = Request(URL+'/message/send', data=send_message_data, headers={'Content-Type':'application/json'})
message_payload = urlopen(message_req)
message_id = int(message_payload['message_id'])


# POST:/message/react
def test_message_react():
    u_id, token = get_user("user1")
    owner_id, owner_token = get_user("user2")
    channel_id = create_channel(token,"Example Channel",1,1)

    data_react = dumps({'token':token, 'message_id': message_id, 'react_id':1, }).encode('utf-8')
    req = Request(URL+'/message/react', data=data_react, headers={'Content-Type':'application/json'}, method='POST')
    payload = urlopen(req)
    assert payload == {}

# POST:/message/unreact
def test_message_unreact():
    data_react = dumps({'token':token, 'message_id': message_id, 'react_id':1, }).encode('utf-8')
    req = Request(URL+'/message/react', data=data_react, headers={'Content-Type':'application/json'}, method='POST')
    payload = urlopen(req)
    req = Request(URL+'/message/unreact', data=data_react, headers={'Content-Type':'application/json'}, method='POST')
    assert urlopen(req) == {}


# POST:/message/pin
def test_message_pin():
    


# POST:/message/unpin
def test_message_unpin():
    pass