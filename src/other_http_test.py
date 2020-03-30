import urllib
import json

BASE_URL = 'http://127.0.0.1:8081'
query_str = 'world'

def test_users_all():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", data={}, headers={'Content-Type': 'application/json'})
    json.load(urllib.request.urlopen(req))

    person1 = register_person()
    person1_token = person1['token']

    response = urllib.request.urlopen(f'{BASE_URL}/users/all?token={person1_token}')
    return_person = json.load(response)

    assert return_person['users'][0]['email'] == 'cs1531@cse.unsw.edu.au'
    assert return_person['users'][0]['handle'] == 'haydenjacobs'
    assert return_person['users'][0]['name_first'] == 'Hayden'
    assert return_person['users'][0]['name_last'] == 'Jacobs'
    assert return_person['users'][0]['permission_id'] == 1
    assert return_person['users'][0]['u_id'] == 1

def test_search():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", data={}, headers={'Content-Type': 'application/json'})
    json.load(urllib.request.urlopen(req))

    person1 = register_person()
    person1_token = person1['token']

    data = json.dumps({
        'token': person1_token,
        'name' : 'Channel 1',
        'is_public' : 'True'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data, headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    new_channel = json.load(response)

    data = json.dumps({
        'token': person1_token,
        'channel_id' : new_channel['channel_id'],
        'message' : 'Hello world'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/send", data=data, headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    json.load(response)

    response = urllib.request.urlopen(f'{BASE_URL}/search?token={person1_token}&query_str=Hello')
    message1_collection = json.load(response)

    assert message1_collection['messages'][0]['message_id'] == 1
    assert message1_collection['messages'][0]['u_id'] == 1
    assert message1_collection['messages'][0]['message'] == 'Hello world'
    #assert message1_collection['messages'][0]['time'] == 0

def register_person():
    data = json.dumps({
        'email': 'cs1531@cse.unsw.edu.au',
        'password': 'abc123',
        'name_first': 'Hayden',
        'name_last': 'Jacobs'
        }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, headers={'Content-Type': 'application/json'})
    response = json.load(urllib.request.urlopen(req))
    return response

def register_person_second():
    data = json.dumps({
        'email': 'cs1532@cse.unsw.edu.au',
        'password': 'abc1234',
        'name_first': 'Hden',
        'name_last': 'Marry'
        }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register",
                                 data=data,
                                 headers={'Content-Type': 'application/json'}
                                )
    response = urllib.request.urlopen(req)
    person = json.load(response)
    return person

def login_person():
    data = json.dumps({
        'email': 'cs1531@cse.unsw.edu.au',
        'password': 'abc123'
        }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login",
                                 data=data,
                                 headers={'Content-Type': 'application/json'}
                                )
    response = urllib.request.urlopen(req)
    login_person_detail = json.load(response)
    return login_person_detail
