from urllib.request import urlopen, Request
from urllib.parse import urlencode
from server import *
from json import loads, dumps
import pytest
from auth import auth_register
from channel import channels_create
from message import message_send
from message_pin_react_functions import message_react, message_pin
from stanup_functions import get_channel_from_channelID, standup_start
from error import InputError, AccessError
from database import getData
import flask
from datetime import datetime

# set up
URL = 'http://127.0.0.1.8009'
email = '123@gmail.com'
password = 'qwertyu1234'
name_first = 'FIRSTNAME'
name_last = 'LASTNAME'
# create a user
u = auth_register(email, password, name_first, name_last)
u_id = u['u_id']
token = u['token']
# create a channel
name = 'CHANNEL_1'
channel_id = channels_create(token, name, True)['channel_id']


# POST: /standup/start
def test_standup_start():
    length = 10
    data = dumps({'token':token, 'channel_id':channel_id, 'length':length}).encode('utf-8')
    req = Request(URL+'/standup/start', data=data, headers={'Content-Type':'application/json'})
    payload = urlopen(req)
    ch = get_channel_from_channelID(channel_id)
    time_finish_stored = ch['standup']['time_finish']
    assert payload['time_finish'] == time_finish_stored
    assert ch['standup']['is_active'] == True

# GET: /standup/active
def test_standup_active():
    standup_start(token, channel_id, 10)
    ch = get_channel_from_channelID(channel_id)
    queryString = urllib.parse.urlencode({
        'token' : token,
        'channel_id': channel_id,
    })
    payload = json.load(urlopen(f"{URL}/standup/actvie?{queryString}"))
    assert payload['is_active'] == actvie
    assert payload['time_finish'] == ch['standup']['time_finish']

# POST: /standup/send
def test_standup_send():
    standup_start(token, channel_id, 10)
    ch = get_channel_from_channelID(channel_id)
    data = dumps({'token':token, 'channel_id':channel_id, 'message':"PENDING_MSG"}).encode('utf-8')
    req = Request(URL+'/standup/send', data=data, headers={'Content-Type':'applicatiion/json'}, method='POST')
    payload = urlopen(req)

    assert payload == {}
    assert ch['standup']['message_buffer'] != [] 




