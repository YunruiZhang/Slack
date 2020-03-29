import urllib
import json
from flask import request
import pytest
BASE_URL = ''

def test_users_all():
    register_person()
    person1 = login_person()
    person1_token = person1['token']
    
    data = json.dumps({
        'token': person1_token
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/other/users_all",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    return_person = json.load(response)
    
    assert(return_person['email'] == 'cs1531@cse.unsw.edu.au')
    assert(return_person['password'] == 'abc123')
    assert(return_person['name_first'] == 'Hayden')
    assert(return_person['name_last'] == 'Jacobs')
    assert(return_person['handle_str'] == 'hjacobs')
    
def test_search():
    register_person()
    person1 = login_person()
    person1_token = person1['token']
    data = json.dumps({
        'token': person1_token,
        'name' : 'Channel 1',
        'is_public' : 'True'
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    new_channel = json.load(response)
    
    data = json.dumps({
        'token': person1_token,
        'channel_id' : new_channel,
        'message' : 'Hello world'
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    message1_id = json.load(response)['message_id']
    
    data = json.dumps({
        'token': person1_token,
        'query_str' = 'Hello'
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/other/search",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    message1_collection = json.load(response)
    
    assert(message1_collection[0]['message_id'] = message1_id)
    assert(message1_collection[0]['u_id'] = person1_u_id)
    assert(message1_collection[0]['message'] = 'Hello world')
    assert(message1_collection[0]['time_created'] = 0)
 
    
def register_person():
    data = json.dumps({
    	'email': 'cs1531@cse.unsw.edu.au'
    	'password': 'abc123'
    	'name_first': 'Hayden'
    	'name_last': 'Jacobs'
    	}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register",
                                 data=data,
                                 headers={'Content-Type': 'application/json'},
                                 )
    response = urllib.request.urlopen(req)
    person = json.load(response)
    return person

def register_person_second():
    data = json.dumps({
    	'email': 'cs1532@cse.unsw.edu.au'
    	'password': 'abc1234'
    	'name_first': 'Hden'
    	'name_last': 'Marry'
    	}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register",
                                 data=data,
                                 headers={'Content-Type': 'application/json'},
                                 )
    response = urllib.request.urlopen(req)
    person = json.load(response)
    return person
    
def login_person():
    data = json.dumps({
    	'email': 'cs1531@cse.unsw.edu.au'
    	'password': 'abc123'
    	}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login",
                                 data=data,
                                 headers={'Content-Type': 'application/json'},
                                 )
    response = urllib.request.urlopen(req)
    login_person = json.load(response)
    return login_person
    

