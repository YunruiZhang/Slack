from urllib.request import urlopen, Request
from server import *
from json import loads, dumps

# set up
URL = 'http://127.0.0.1.8000'
# create a user
user_payload = loads(urlopen(URL + '/auth/register'))
token = user_payload['token']
u_id = int(user_payload['u_id'])
# create a channel
create_channel_data = dumps({'token': token, 'name': 'channel_one', 'is_public': True, }).encode('utf-8')
channel_req = Request(URL+'/channels/create', data=create_channel_data, headers={'Content-Type':'application/json'}, method='POST')
channel_payload = urlopen(channel_req)
channel_id = int(channel_payload['channel_id'])
# send a message
send_message_data = dumps({'token': token, 'channel_id': channel_id, 'message': "FIRST_MESSAGE",}).encode('utf-8')
message_req = Request(URL+'/message/send', data=send_message_data, headers={'Content-Type':'application/json'}, method='POST')
message_payload = urlopen(message_req)
message_id = int(message_payload['message_id'])


# POST:/message/react
def test_message_react():
    data_react = dumps({'token':token, 'message_id': message_id, 'react_id':1, }).encode('utf-8')
    req = Request(URL+'/message/react', data=data_react, headers={'Content-Type':'application/json'}, method='POST')
    payload = urlopen(req)
    assert payload == {}

# POST:/message/
def test_message_unreact():
    pass


# POST:/message/
def test_message_pin():
    pass


# POST:/message/
def test_message_unpin():
    pass