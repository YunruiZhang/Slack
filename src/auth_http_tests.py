'''
This file contains the test methods for the server.py methods
that are associated to the auth file
'''
import urllib
import json
from flask import request

BASE_URL = "http://127.0.0.1:8080"

def test_register():
    '''
    This test method will try and create a user using the an email,
    password, and name.  If the output of the flask methods are not null,
    then an id and token were created for the user which indicates a 
    successful registration of the user
    '''
    data = json.dumps({
    	'email': 'paul@gmail.com',
    	'password': '123password',
    	'name_first': 'Paul',
    	'name_last': 'Velliotis'
    	}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register",
                                data=data,
                                headers={'Content-Type': 'application/json'},
                                method='POST')
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    assert (payload['u_id'] is not None) and (payload['token'] is not None)

