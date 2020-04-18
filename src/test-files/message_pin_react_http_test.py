import urllib
import json
from server import *


# set up
URL = 'http://127.0.0.1:8081'
email = '1234@gmail.com'
password = 'qwertyu1234'
name_first = 'FIRSTNAME'
name_last = 'LASTNAME'

# POST:/message/react
def test_message_react_and_pins():
    req = urllib.request.Request(f"{URL}/workspace/reset", data={}, headers={'Content-Type': 'application/json'})
    json.load(urllib.request.urlopen(req))

    data = json.dumps({
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    }).encode('utf-8')

    req = urllib.request.Request(f"{URL}/auth/register", data=data, headers={'Content-Type': 'application/json'}, method='POST')
    response = json.load(urllib.request.urlopen(req))

    u_id = response['u_id']
    token = response['token']

    # create a channel
    #name = 'CHANNEL_1'
    #channel_id = channels_create(token, name, True)['channel_id']
    create_data = json.dumps({
        "token" : token,
        "name" : "CHANNEL_1",
        "is_public" : True
    }).encode('utf-8')

    req = urllib.request.Request(f"{URL}/channels/create", data=create_data, headers={'Content-Type': 'application/json'})
    channel_id_to_invite = json.load(urllib.request.urlopen(req))

    channel_id = channel_id_to_invite['channel_id']

    # create a message

    data = json.dumps({
        'token': token,
        'channel_id': channel_id,
        'message': 'NEWMESSAGE'
    }).encode('utf-8')
    req = urllib.request.Request(f"{URL}/message/send", data=data, headers={'Content-Type': 'application/json'})
    message_returned = json.load(urllib.request.urlopen(req))

    message_id = message_returned['message_id']
    data = json.dumps({
        'token':token,
        'message_id': message_id,
        'react_id':1
    }).encode('utf-8')

    req = urllib.request.Request(f"{URL}/message/react", data=data, headers={'Content-Type':'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    print(payload)

    assert payload == {}

# POST:/message/unreact
    req = urllib.request.Request(f"{URL}/message/unreact", data=data, headers={'Content-Type':'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}


# POST:/message/pin
    req = urllib.request.Request(f"{URL}/message/pin", data=data, headers={'Content-Type':'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

# POST:/message/unpin
    req = urllib.request.Request(f"{URL}/message/unpin", data=data, headers={'Content-Type':'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}
