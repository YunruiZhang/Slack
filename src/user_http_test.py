import urllib
import json
from flask import request
import pytest
BASE_URL = 'http://127.0.0.1:8081'

def test_user_profile():
    
    register_person()
    person1 = login_person()
    person1_token = person1['token']
    person1_u_id = person1['u_id']
    response = urllib.request.urlopen(f'{BASE_URL}/user/profile?token={person1_token}&u_id={person1_u_id}')
    return_person = json.load(response)
    
    assert(return_person['email'] == 'cs1531@cse.unsw.edu.au')
    assert(return_person['password'] == 'abc123')
    assert(return_person['name_first'] == 'Hayden')
    assert(return_person['name_last'] == 'Jacobs')
    
 
    response = urllib.request.urlopen(f'{BASE_URL}/user/profile?token={person1_token}&u_id={10000000}')
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req))
        
def test_user_profile_setname():
    
    #register_person()
    person1 = login_person()
    person1_token = person1['token']
    data = json.dumps({
        'token': person1_token,  
        'name_first' : 'Python',
        'name_last' : 'Forever' 
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setname",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
   
    person2 = urllib_request_user_profile(person1_token,person1['u_id'])
    
    assert(person2['name_first'] == 'Python')
    assert(person2['name_last'] == 'Forever')
    
    data2 = json.dumps({
        'token': person1_token,
        'name_first' : 'n'*100,
        'name_last' : 'Forever' 
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setname",
                                 data=data2,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req))
        
    data3 = json.dumps({
        'token': person1_token, 
        'name_first' : 'Python',
        'name_last' : 'F' * 100
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setname",
                                 data=data3,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req))    

def test_user_profile_setemail():
    
    #register_person()
    person1 = login_person()
    person1_token = person1['token']
    data = json.dumps({
        'token': person1_token, 
        'email': 'cs1533@cse.unsw.edu.au' 
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setemail",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    person1 = urllib_request_user_profile(person1_token,person1['u_id'])
    assert person1['email'] == 'cs1533@cse.unsw.edu.au'
    
    register_person_second()
    person2 = login_person_second()
    person2_token = person2['token']
    data = json.dumps({
        'token': person1_token, 
        'email': 'cs1532@cse.unsw.edu.au' 
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setemail",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req)) 
        
    data = json.dumps({
        'token': person1_token, 
        'email': '11111111' 
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setemail",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req))
    
def test_user_profile_sethandle():
    
    #register_person()
    person1 = login_person()
    person1_token = person1['token']
    data = json.dumps({
        'token': person1_token, 
        'handle': 'lovepython' 
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_sethandle",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    person2 = urllib_request_user_profile(person1_token,person1['u_id'])
    assert person1['handle'] == 'lovepython'
    
    #register_person_second()
    person2 = login_person_second()
    data = json.dumps({
        'token': person1_token, 
        'handle': 'hdenmarry' 
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_sethandle",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req)) 
        
    data = json.dumps({
        'token': person1_token, 
        'email': 'a' 
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_sethandle",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req)) 

def urllib_request_user_profile(token,u_id):
    response = urllib.request.urlopen(f'{BASE_URL}/user/profile?token={token}&u_id={u_id}')
    return_person = json.load(response)
    return return_person


def register_person():
    data = json.dumps({
    	'email': 'cs1531@cse.unsw.edu.au',
    	'password': 'abc123',
    	'name_first': 'Hayden',
    	'name_last': 'Jacobs'
    	}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register",
                                 data=data,
                                 headers={'Content-Type': 'application/json'},
                                 method='POST'
                                 )
    response = urllib.request.urlopen(req)
    person = json.load(response)
    return person

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
    login_person = json.load(response)
    return login_person
    
def login_person_second():
    data = json.dumps({
    	'email': 'cs1532@cse.unsw.edu.au',
    	'password': 'abc1234'
    	}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login",
                                 data=data,
                                 headers={'Content-Type': 'application/json'}
                                 )
    response = urllib.request.urlopen(req)
    login_person = json.load(response)
    return login_person