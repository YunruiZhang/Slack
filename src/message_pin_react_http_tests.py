from urllib.request import urlopen, Request
from server import *
from json import loads, dumps
import pytest
from auth import auth_register
from channel import channels_create
from message import message_send
from message_pin_react_functions import message_react, message_pin
from error import InputError, AccessError
from database import getData
import flask



# set up
URL = 'http://127.0.0.1.8000'
email = '123@gmail.com'
password = 'qwertyu1234'
name_first = 'FIRSTNAME'
name_last = 'LASTNAME'
D = getData()
# create a user
u = auth_register(email, password, name_first, name_last)
u_id = u['u_id']
token = u['token']
# create a channel
name = 'CHANNEL_1'
channel_id = channels_create(token, name, True)['channel_id']
# create a message
message = 'NEWMESSAGE'
message_id = message_send(token, channel_id, message)['message_id']


# POST:/message/react
def test_message_react():
    data = dumps({'token':token, 'message_id': message_id, 'react_id':1 }).encode('utf-8')
    req = Request(URL+'/message/react', data=data, headers={'Content-Type':'application/json'}, method='POST')
    payload = urlopen(req)
    assert payload == {}

# POST:/message/unreact
def test_message_unreact():
    message_react(token, message_id, react_id)
    data = dumps({'token':token, 'message_id': message_id, 'react_id':1 }).encode('utf-8')
    req = Request(URL+'/message/unreact', data=data, headers={'Content-Type':'application/json'}, method='POST')
    assert urlopen(req) == {}


# POST:/message/pin
def test_message_pin():
    data = dumps({'token':token, 'message_id': message_id }).encode('utf-8')
    req = Request(URL+'/message/pin', data=data, headers={'Content-Type':'application/json'}, method='POST')
    assert urlopen(req) == {}

# POST:/message/unpin
def test_message_unpin():
    message_pin(token, message_id)
    data = dumps({'token':token, 'message_id': message_id }).encode('utf-8')
    req = Request(URL+'/message/unpin', data=data, headers={'Content-Type':'application/json'}, method='POST')
    assert urlopen(req) == {}


