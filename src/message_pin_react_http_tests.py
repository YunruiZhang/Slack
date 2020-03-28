from urllib.request import urlopen, Request
from server import *
from json import loads, dumps
import pytest
from auth import auth_register
from error import InputError, AccessError
from database import getData


# set up
URL = 'http://127.0.0.1.8000'
email = '123@gmail.com'
password = 'qwertyu1234'
name_first = 'FIRSTNAME'
name_last = 'LASTNAME'
# create a user
u = auth_register(email, password, name_first, name_last)
u_id = u['u_id']

# create a channel

# create a message



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
    pass


# POST:/message/unpin
def test_message_unpin():
    pass