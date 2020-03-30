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
from urllib.error import HTTPError
from datetime import datetime
BASE_URL = 'http://127.0.0.1:8081'

def test_message_send():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))
    #test send
    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)

    data = json.dumps({
        'token': token,
        'channel_id': channel_id,
        'message': 'test'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/send", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload['message_id'] is not None

    #test remove 
    data2 = json.dumps({
        'token': token,
        'message_id': 1,
    }).encode('utf-8')
   
    req = urllib.request.Request(f"{BASE_URL}/message/remove", data=data2, headers={'Content-Type': 'application/json'}, method='DELETE')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

    #send another message
    req = urllib.request.Request(f"{BASE_URL}/message/send", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    #edit the message
    data3 = json.dumps({
        'token': token,
        'message_id': 1,
        'message': 'yep'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/edit", data=data3, headers={'Content-Type': 'application/json'}, method='PUT')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}
    #test send later
    time = datetime.now()
    data4 = json.dumps({
        'token': token,
        'channel_id': channel_id,
        'message': 'yep',
        'time_sent': str(time)
    }).encode('utf-8')
    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/message/sendlater", data=data4, headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))
    


def get_user(username):
    data = json.dumps({
    	'email': username + '@gmail.com',
        'password': 'passno',
    	'name_first': 'Paul',
    	'name_last': 'Velliotis'
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, headers={'Content-Type': 'application/json'}, method='POST')
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    return payload['u_id'], payload['token']



def create_channel(token,name,public,return_id):

    create_data = json.dumps({
        "token" : token,
        "name" : name,
        "is_public" : public
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=create_data,headers={'Content-Type': 'application/json'})
    channel_id_to_invite = json.load(urllib.request.urlopen(req))

    if return_id:
        return channel_id_to_invite['channel_id']
    else:
        return channel_id_to_invite
