import urllib
import json
from flask import request
import pytest
BASE_URL = ''

def test_user_profile():
    
    register_person()
    person1 = login_person()
    person1_token = person1['token']
    data = json.dumps({
        'token': person1_token
        'u_id' : person1['u_id']   
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    return_person = json.load(response)
    
    assert(return_person['email'] == 'cs1531@cse.unsw.edu.au')
    assert(return_person['password'] == 'abc123')
    assert(return_person['name_first'] == 'Hayden')
    assert(return_person['name_last'] == 'Jacobs')
    
    data1 = json.dumps({
        'token': person1_token
        'u_id' : 100000000   
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile",
        data=data1, 
        headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req))
        
def test_user_profile_setname():
    
    register_person()
    person1 = login_person()
    person1_token = person1['token']
    data = json.dumps({
        'token': person1_token  
        'name_first' : 'Python'
        'name_last' : 'Forever' 
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setname",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    data1 = json.dumps({
        'token': person1_token
        'u_id' : person1['u_id']  
    })ecode('utf-8')
    person2 = urllib_request_user_profile(data1)
    
    assert(person2['name_first'] == 'Python')
    assert(person2['name_last'] == 'Forever')
    
    data2 = json.dumps({
        'token': person1_token 
        'name_first' : 'n'*100
        'name_last' : 'Forever' 
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setname",
                                 data=data2,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req))
        
    data3 = json.dumps({
        'token': person1_token 
        'name_first' : 'Python'
        'name_last' : 'F' * 100
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setname",
                                 data=data3,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req))    

def test_user_profile_setemail():
    
    register_person()
    person1 = login_person()
    person1_token = person1['token']
    data = json.dumps({
        'token': person1_token 
        'email': 'cs1533@cse.unsw.edu.au' 
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setemail",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    data = json.dumps({
        'token': person1_token 
        'u_id': person1['u_id'] 
    })ecode('utf-8')
    person1 = urllib_request_user_profile(data)
    assert person1['email'] = 'cs1533@cse.unsw.edu.au'
    
    register_person_second()
    person2 = login_person_second()
    person2_token = person2['token']
    data = json.dumps({
        'token': person1_token 
        'email': 'cs1532@cse.unsw.edu.au' 
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setemail",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req)) 
        
    data = json.dumps({
        'token': person1_token 
        'email': '11111111' 
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_setemail",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req))
    
def test_user_profile_sethandle():
    
    register_person()
    person1 = login_person()
    person1_token = person1['token']
    data = json.dumps({
        'token': person1_token 
        'handle': 'lovepython' 
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_sethandle",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    data = json.dumps({
        'token': person1_token 
        'u_id': person1['u_id'] 
    })ecode('utf-8')
    person1 = urllib_request_user_profile(data)
    assert person1['handle'] = 'lovepython'
    
    register_person_second()
    person2 = login_person_second()
    data = json.dumps({
        'token': person1_token 
        'handle': 'hdenmarry' 
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_sethandle",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req)) 
        
    data = json.dumps({
        'token': person1_token 
        'email': 'a' 
    })ecode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile_sethandle",
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
    with pytest.raises(HTTPError) as e:
        json.load(urllib.request.urlopen(req)) 

def urllib_request_user_profile(data):
    req = urllib.request.Request(f"{BASE_URL}/user/user_profile",
                                 data=data1,
                                 headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    return_person = json.load(response)
    return return_person


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
    
def login_person_second():
    data = json.dumps({
    	'email': 'cs1532@cse.unsw.edu.au'
    	'password': 'abc1234'
    	}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login",
                                 data=data,
                                 headers={'Content-Type': 'application/json'},
                                 )
    response = urllib.request.urlopen(req)
    login_person = json.load(response)
    return login_person
